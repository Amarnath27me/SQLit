"""
Test all solution queries against their respective datasets.
Runs each problem's solution_query and reports failures.

Usage:  cd backend && python test_all_solutions.py
"""
import sys
import os
import sqlite3
import re
import time
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.services.problem_service import get_all_problems
from app.services.query_executor import _get_dataset_sql, _pg_to_sqlite


# ── Extended PG → SQLite conversion for solution queries ────────────
def pg_solution_to_sqlite(sql: str) -> str:
    """Convert PostgreSQL solution queries to SQLite-compatible SQL."""
    # First apply the standard conversion
    sql = _pg_to_sqlite(sql)

    # TO_CHAR(col, 'YYYY-MM') → strftime('%Y-%m', col)
    def replace_to_char(match):
        col = match.group(1).strip()
        fmt = match.group(2).strip().strip("'\"")
        sqlite_fmt = (
            fmt.replace("YYYY", "%Y")
            .replace("YY", "%y")
            .replace("MM", "%m")
            .replace("DD", "%d")
            .replace("HH24", "%H")
            .replace("HH", "%H")
            .replace("MI", "%M")
            .replace("SS", "%S")
            .replace("Month", "%m")
            .replace("Day", "%d")
            .replace("Mon", "%m")
            .replace("Dy", "%d")
        )
        return f"strftime('{sqlite_fmt}', {col})"
    sql = re.sub(
        r"TO_CHAR\s*\(\s*([^,]+?)\s*,\s*'([^']+)'\s*\)",
        replace_to_char, sql, flags=re.IGNORECASE
    )

    # EXTRACT(YEAR FROM col) → CAST(strftime('%Y', col) AS INTEGER)
    def replace_extract(match):
        part = match.group(1).strip().upper()
        col = match.group(2).strip()
        fmt_map = {"YEAR": "%Y", "MONTH": "%m", "DAY": "%d", "HOUR": "%H",
                    "MINUTE": "%M", "SECOND": "%S", "DOW": "%w", "DOY": "%j",
                    "EPOCH": "%s"}
        fmt = fmt_map.get(part, "%Y")
        return f"CAST(strftime('{fmt}', {col}) AS INTEGER)"
    sql = re.sub(
        r"EXTRACT\s*\(\s*(\w+)\s+FROM\s+([^)]+)\)",
        replace_extract, sql, flags=re.IGNORECASE
    )

    # DATE_TRUNC('month', col) → date(col, 'start of month')
    def replace_date_trunc(match):
        part = match.group(1).strip().strip("'\"").lower()
        col = match.group(2).strip()
        if part == "month":
            return f"date({col}, 'start of month')"
        elif part == "year":
            return f"strftime('%Y-01-01', {col})"
        elif part == "day":
            return f"date({col})"
        elif part == "week":
            return f"date({col}, 'weekday 0', '-6 days')"
        return f"date({col})"
    sql = re.sub(
        r"DATE_TRUNC\s*\(\s*'(\w+)'\s*,\s*([^)]+)\)",
        replace_date_trunc, sql, flags=re.IGNORECASE
    )

    # STRING_AGG(col, ', ') → GROUP_CONCAT(col, ', ')
    sql = re.sub(r'\bSTRING_AGG\s*\(', 'GROUP_CONCAT(', sql, flags=re.IGNORECASE)

    # col::TEXT, col::INTEGER, etc → CAST(col AS TEXT)
    def replace_cast_shorthand(match):
        col = match.group(1)
        typ = match.group(2).upper()
        if typ in ("TEXT", "VARCHAR"):
            return f"CAST({col} AS TEXT)"
        elif typ in ("INTEGER", "INT", "BIGINT"):
            return f"CAST({col} AS INTEGER)"
        elif typ in ("REAL", "FLOAT", "DOUBLE", "NUMERIC", "DECIMAL"):
            return f"CAST({col} AS REAL)"
        return f"CAST({col} AS {typ})"
    sql = re.sub(r'(\w+(?:\([^)]*\))?)\s*::\s*(\w+)', replace_cast_shorthand, sql, flags=re.IGNORECASE)

    # AGE(date1, date2) → (julianday(date1) - julianday(date2))
    sql = re.sub(
        r'\bAGE\s*\(\s*([^,]+),\s*([^)]+)\)',
        r'(julianday(\1) - julianday(\2))',
        sql, flags=re.IGNORECASE
    )

    # CURRENT_DATE → date('now')
    sql = re.sub(r'\bCURRENT_DATE\b', "date('now')", sql, flags=re.IGNORECASE)
    # CURRENT_TIMESTAMP → datetime('now')
    sql = re.sub(r'\bCURRENT_TIMESTAMP\b', "datetime('now')", sql, flags=re.IGNORECASE)

    # INTERVAL '30 days' → just the number for julianday math
    sql = re.sub(r"INTERVAL\s+'(\d+)\s+days?'", r"'\1 days'", sql, flags=re.IGNORECASE)

    # bool comparisons: = TRUE → = 1, = FALSE → = 0
    sql = re.sub(r'\bTRUE\b', '1', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bFALSE\b', '0', sql, flags=re.IGNORECASE)

    # COALESCE is supported in SQLite, no change needed
    # CASE WHEN is supported in SQLite, no change needed

    # ILIKE → LIKE (SQLite LIKE is case-insensitive for ASCII by default)
    sql = re.sub(r'\bILIKE\b', 'LIKE', sql, flags=re.IGNORECASE)

    # GENERATE_SERIES — not supported, skip these
    # LATERAL — not supported, skip these
    # FILTER (WHERE ...) — not supported directly

    return sql


def create_sqlite_db(dataset: str) -> sqlite3.Connection:
    """Create an in-memory SQLite database with dataset loaded."""
    conn = sqlite3.connect(":memory:")
    schema_sql, seed_sql = _get_dataset_sql(dataset)
    if schema_sql:
        conn.executescript(_pg_to_sqlite(schema_sql))
    if seed_sql:
        conn.executescript(_pg_to_sqlite(seed_sql))
    return conn


def test_all():
    problems = get_all_problems()
    print(f"\nTesting {len(problems)} solution queries...\n")

    # Pre-create databases for each dataset
    dbs = {}
    for dataset in ["ecommerce", "finance", "healthcare"]:
        try:
            dbs[dataset] = create_sqlite_db(dataset)
            print(f"  OK Loaded {dataset} dataset")
        except Exception as e:
            print(f"  FAIL Failed to load {dataset}: {e}")

    print()

    passed = 0
    failed = []
    skipped = []

    # Known PG-only features that can't work in SQLite
    pg_only_keywords = [
        "GENERATE_SERIES", "LATERAL", "FILTER (WHERE", "FILTER(WHERE",
        "PERCENTILE_CONT", "PERCENTILE_DISC", "ARRAY_AGG", "UNNEST",
        "RECURSIVE", "WITH RECURSIVE", "CROSSTAB", "TABLESAMPLE",
        "GROUPING SETS", "ROLLUP", "CUBE",
    ]

    for p in problems:
        pid = p["id"]
        dataset = p.get("dataset", "ecommerce")
        solution = p.get("solution_query", "")

        if not solution.strip():
            skipped.append((pid, "No solution query"))
            continue

        # Check for PostgreSQL-only features
        upper_sol = solution.upper()
        pg_only = False
        for kw in pg_only_keywords:
            if kw.upper() in upper_sol:
                skipped.append((pid, f"Uses PG-only feature: {kw}"))
                pg_only = True
                break
        if pg_only:
            continue

        if dataset not in dbs:
            skipped.append((pid, f"Dataset {dataset} not loaded"))
            continue

        # Convert PG solution to SQLite
        sqlite_query = pg_solution_to_sqlite(solution)

        try:
            cursor = dbs[dataset].execute(sqlite_query)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            if len(rows) == 0:
                # Zero rows might be valid for some queries, but flag it
                failed.append((pid, p["title"], p["difficulty"], "Returns 0 rows", sqlite_query))
            else:
                passed += 1
        except Exception as e:
            error = str(e).split("\n")[0]
            failed.append((pid, p["title"], p["difficulty"], error, sqlite_query))

    # Close DBs
    for conn in dbs.values():
        conn.close()

    # Report
    print(f"{'='*80}")
    print(f"RESULTS: {passed} passed | {len(failed)} failed | {len(skipped)} skipped (PG-only)")
    print(f"{'='*80}")

    if skipped:
        print(f"\n--- SKIPPED ({len(skipped)}) ---")
        for pid, reason in skipped:
            print(f"  {pid}: {reason}")

    if failed:
        print(f"\n--- FAILED ({len(failed)}) ---")
        for pid, title, diff, error, query in failed:
            print(f"\n  [{diff.upper()}] {pid}: {title}")
            print(f"    Error: {error}")
            # Print first 2 lines of query for context
            qlines = query.strip().split("\n")[:3]
            for ql in qlines:
                print(f"    Query: {ql}")

    return failed


if __name__ == "__main__":
    failed = test_all()
    sys.exit(1 if failed else 0)
