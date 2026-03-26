"""
Sandboxed SQL query execution service.

Uses PostgreSQL schemas for isolation: each execution creates a temporary schema,
loads the dataset, runs the query, then drops the schema.
For local dev without PostgreSQL, falls back to SQLite in-memory.
"""

import asyncio
import logging
import re
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

from app.core.config import settings


# ---------------------------------------------------------------------------
# PostgreSQL availability cache
# ---------------------------------------------------------------------------

_pg_check_cache: dict = {"available": None, "checked_at": 0}


def _pg_available() -> bool:
    """Check if PostgreSQL sandbox database is reachable. Caches result for 60s."""
    now = time.time()
    if _pg_check_cache["available"] is not None and now - _pg_check_cache["checked_at"] < 60:
        return _pg_check_cache["available"]

    try:
        import psycopg2
        conn = psycopg2.connect(settings.sandbox_database_url, connect_timeout=2)
        conn.close()
        _pg_check_cache["available"] = True
    except Exception:
        _pg_check_cache["available"] = False
    _pg_check_cache["checked_at"] = now
    return _pg_check_cache["available"]


def _get_dataset_sql(dataset: str) -> tuple[str, str]:
    """Load schema + seed SQL for a dataset.

    Tries seed.sql first; falls back to the package's get_seed_sql() generator.
    """
    base = Path(__file__).parent.parent / "datasets" / dataset
    schema_path = base / "schema.sql"
    seed_path = base / "seed.sql"

    schema_sql = schema_path.read_text() if schema_path.exists() else ""

    if seed_path.exists():
        seed_sql = seed_path.read_text()
    else:
        # Fall back to dynamic seed generation from the dataset package
        try:
            import importlib
            mod = importlib.import_module(f"app.datasets.{dataset}")
            seed_sql = mod.get_seed_sql()
        except (ImportError, AttributeError):
            seed_sql = ""

    return schema_sql, seed_sql


# ---------------------------------------------------------------------------
# PostgreSQL sandbox
# ---------------------------------------------------------------------------


def _mysql_to_pg(sql: str) -> str:
    """Convert MySQL-specific syntax to PostgreSQL-compatible SQL."""
    # Backtick → double quotes
    sql = sql.replace('`', '"')
    # IFNULL → COALESCE
    sql = re.sub(r'\bIFNULL\s*\(', 'COALESCE(', sql, flags=re.IGNORECASE)
    # LIMIT x, y → LIMIT y OFFSET x
    sql = re.sub(r'LIMIT\s+(\d+)\s*,\s*(\d+)', r'LIMIT \2 OFFSET \1', sql, flags=re.IGNORECASE)

    # GROUP_CONCAT(col SEPARATOR ',') → STRING_AGG(col::text, ',')
    def _replace_group_concat(match):
        content = match.group(1).strip()
        sep_match = re.search(r'\bSEPARATOR\s+([\'"][^\'"]*[\'"])', content, re.IGNORECASE)
        if sep_match:
            col = content[:sep_match.start()].strip()
            sep = sep_match.group(1)
            return f'STRING_AGG({col}::text, {sep})'
        return f"STRING_AGG({content}::text, ',')"
    sql = re.sub(r'GROUP_CONCAT\s*\(([^)]+)\)', _replace_group_concat, sql, flags=re.IGNORECASE)

    # DATE_FORMAT(col, fmt) → TO_CHAR(col, pg_fmt)
    def _replace_date_format(match):
        col = match.group(1).strip()
        fmt = match.group(2).strip().strip("'\"")
        pg_fmt = (
            fmt
            .replace('%Y', 'YYYY')
            .replace('%m', 'MM')
            .replace('%d', 'DD')
            .replace('%H', 'HH24')
            .replace('%i', 'MI')
            .replace('%s', 'SS')
        )
        return f"TO_CHAR({col}, '{pg_fmt}')"
    sql = re.sub(
        r'DATE_FORMAT\s*\(\s*([^,]+),\s*([^)]+)\)',
        _replace_date_format,
        sql,
        flags=re.IGNORECASE,
    )
    return sql


@contextmanager
def _pg_sandbox(dataset: str):
    """Create an isolated PostgreSQL schema for sandboxed execution."""
    import psycopg2

    schema_name = f"sandbox_{uuid.uuid4().hex[:12]}"
    conn = None
    try:
        conn = psycopg2.connect(settings.sandbox_database_url)
        conn.autocommit = False
        cursor = conn.cursor()

        # Create isolated schema
        cursor.execute(f'CREATE SCHEMA "{schema_name}"')
        cursor.execute(f'SET search_path TO "{schema_name}"')

        # Load dataset
        schema_sql, seed_sql = _get_dataset_sql(dataset)
        if schema_sql:
            cursor.execute(schema_sql)
        if seed_sql:
            cursor.execute(seed_sql)
        conn.commit()

        yield cursor, conn
    finally:
        if conn:
            try:
                conn.rollback()
                cur = conn.cursor()
                cur.execute(f'DROP SCHEMA IF EXISTS "{schema_name}" CASCADE')
                conn.commit()
            except Exception:
                pass
            finally:
                conn.close()


def execute_query_pg_sync(
    query: str,
    dataset: str,
    dialect: str = "postgresql",
    timeout_seconds: int = 3,
    max_rows: int = 1000,
) -> dict:
    """Execute a SELECT query in a sandboxed PostgreSQL schema."""
    if dialect == "mysql":
        query = _mysql_to_pg(query)

    try:
        with _pg_sandbox(dataset) as (cursor, conn):
            start = time.perf_counter()
            # Set statement timeout (milliseconds)
            cursor.execute(f"SET statement_timeout = '{timeout_seconds * 1000}'")
            cursor.execute(query)

            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchmany(max_rows)
            elapsed = (time.perf_counter() - start) * 1000

            return {
                "success": True,
                "columns": columns,
                "rows": [list(row) for row in rows],
                "row_count": len(rows),
                "execution_time_ms": round(elapsed, 2),
            }
    except Exception as e:
        # Sanitize: only return safe SQL error info, not internal details
        error_msg = str(e)
        # Strip connection/system info, keep SQL-relevant error
        if "relation" in error_msg or "column" in error_msg or "syntax" in error_msg.lower():
            safe_error = error_msg.split("\n")[0]  # First line only
        else:
            safe_error = "Query execution failed. Check your SQL syntax and try again."
            logger.warning("Query execution error (sanitized): %s", error_msg)
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "execution_time_ms": 0,
            "error": safe_error,
        }


# ---------------------------------------------------------------------------
# SQLite sandbox (fallback)
# ---------------------------------------------------------------------------


@contextmanager
def _sqlite_sandbox(dataset: str):
    """Create an in-memory SQLite database loaded with dataset."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    schema_sql, seed_sql = _get_dataset_sql(dataset)

    if schema_sql:
        # Convert PostgreSQL syntax to SQLite-compatible
        sqlite_schema = _pg_to_sqlite(schema_sql)
        conn.executescript(sqlite_schema)

    if seed_sql:
        sqlite_seed = _pg_to_sqlite(seed_sql)
        conn.executescript(sqlite_seed)

    try:
        yield conn
    finally:
        conn.close()


def _pg_to_sqlite(sql: str) -> str:
    """Basic PostgreSQL → SQLite syntax conversion."""
    import re
    sql = re.sub(r'SERIAL\b', 'INTEGER', sql, flags=re.IGNORECASE)
    sql = re.sub(r'BIGSERIAL\b', 'INTEGER', sql, flags=re.IGNORECASE)
    sql = re.sub(r'VARCHAR\(\d+\)', 'TEXT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'TIMESTAMP\b', 'TEXT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'BOOLEAN\b', 'INTEGER', sql, flags=re.IGNORECASE)
    sql = re.sub(r'DECIMAL\(\d+,\s*\d+\)', 'REAL', sql, flags=re.IGNORECASE)
    sql = re.sub(r'NUMERIC\(\d+,\s*\d+\)', 'REAL', sql, flags=re.IGNORECASE)
    sql = re.sub(r'NOW\(\)', "datetime('now')", sql, flags=re.IGNORECASE)
    # Remove PostgreSQL-specific clauses
    sql = re.sub(r'ON CONFLICT.*?;', ';', sql, flags=re.IGNORECASE | re.DOTALL)
    return sql


def _mysql_to_sqlite(sql: str) -> str:
    """Convert MySQL-specific syntax to SQLite-compatible SQL."""
    import re
    # IFNULL → same in SQLite (SQLite supports IFNULL)
    # No conversion needed for IFNULL

    # CONCAT('a', 'b') → 'a' || 'b'
    # Simple case: CONCAT(a, b) → a || b
    # Handle CONCAT with multiple args
    def replace_concat(match):
        args = match.group(1)
        parts = [a.strip() for a in args.split(',')]
        return ' || '.join(parts)
    sql = re.sub(r'CONCAT\s*\(([^)]+)\)', replace_concat, sql, flags=re.IGNORECASE)

    # NOW() → datetime('now')
    sql = re.sub(r'\bNOW\s*\(\)', "datetime('now')", sql, flags=re.IGNORECASE)

    # CURDATE() → date('now')
    sql = re.sub(r'\bCURDATE\s*\(\)', "date('now')", sql, flags=re.IGNORECASE)

    # DATE_FORMAT(col, '%Y-%m') → strftime('%Y-%m', col)
    def replace_date_format(match):
        col = match.group(1).strip()
        fmt = match.group(2).strip()
        return f"strftime({fmt}, {col})"
    sql = re.sub(r'DATE_FORMAT\s*\(\s*([^,]+),\s*([^)]+)\)', replace_date_format, sql, flags=re.IGNORECASE)

    # DATEDIFF(a, b) → CAST(julianday(a) - julianday(b) AS INTEGER)
    sql = re.sub(
        r'DATEDIFF\s*\(\s*([^,]+),\s*([^)]+)\)',
        r'CAST(julianday(\1) - julianday(\2) AS INTEGER)',
        sql, flags=re.IGNORECASE
    )

    # YEAR(col) → CAST(strftime('%Y', col) AS INTEGER)
    sql = re.sub(r'\bYEAR\s*\(\s*([^)]+)\)', r"CAST(strftime('%Y', \1) AS INTEGER)", sql, flags=re.IGNORECASE)

    # MONTH(col) → CAST(strftime('%m', col) AS INTEGER)
    sql = re.sub(r'\bMONTH\s*\(\s*([^)]+)\)', r"CAST(strftime('%m', \1) AS INTEGER)", sql, flags=re.IGNORECASE)

    # DAY(col) → CAST(strftime('%d', col) AS INTEGER)
    sql = re.sub(r'\bDAY\s*\(\s*([^)]+)\)', r"CAST(strftime('%d', \1) AS INTEGER)", sql, flags=re.IGNORECASE)

    # LIMIT x, y → LIMIT y OFFSET x (MySQL uses LIMIT offset, count)
    sql = re.sub(r'LIMIT\s+(\d+)\s*,\s*(\d+)', r'LIMIT \2 OFFSET \1', sql, flags=re.IGNORECASE)

    # GROUP_CONCAT(col SEPARATOR ',') → GROUP_CONCAT(col, ',')
    def replace_group_concat(match):
        content = match.group(1).strip()
        sep_match = re.search(r'\bSEPARATOR\s+([\'"][^\'"]*[\'"])', content, re.IGNORECASE)
        if sep_match:
            col = content[:sep_match.start()].strip()
            sep = sep_match.group(1)
            return f'GROUP_CONCAT({col}, {sep})'
        return f'GROUP_CONCAT({content})'
    sql = re.sub(r'GROUP_CONCAT\s*\(([^)]+)\)', replace_group_concat, sql, flags=re.IGNORECASE)

    # SUBSTRING → SUBSTR (SQLite uses SUBSTR)
    sql = re.sub(r'\bSUBSTRING\s*\(', 'SUBSTR(', sql, flags=re.IGNORECASE)

    # Remove backtick quoting (MySQL style) → no quoting
    sql = sql.replace('`', '')

    # BOOLEAN/TINYINT(1) TRUE/FALSE → 1/0
    sql = re.sub(r'\bTRUE\b', '1', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bFALSE\b', '0', sql, flags=re.IGNORECASE)

    return sql


def execute_query_sync(
    query: str,
    dataset: str,
    dialect: str = "postgresql",
    timeout_seconds: int = 3,
    max_rows: int = 1000,
) -> dict:
    """Execute a SELECT query in a sandboxed SQLite database."""
    if dialect == "mysql":
        query = _mysql_to_sqlite(query)

    with _sqlite_sandbox(dataset) as conn:
        start = time.perf_counter()
        try:
            cursor = conn.execute(query)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchmany(max_rows)
            elapsed = (time.perf_counter() - start) * 1000

            return {
                "success": True,
                "columns": columns,
                "rows": [list(row) for row in rows],
                "row_count": len(rows),
                "execution_time_ms": round(elapsed, 2),
            }
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            error_msg = str(e)
            if "relation" in error_msg or "column" in error_msg or "syntax" in error_msg.lower():
                safe_error = error_msg.split("\n")[0]
            else:
                safe_error = "Query execution failed. Check your SQL syntax and try again."
                logger.warning("Sandboxed query error (sanitized): %s", error_msg)
            return {
                "success": False,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "execution_time_ms": round(elapsed, 2),
                "error": safe_error,
            }


async def execute_sandboxed_query(
    query: str,
    dataset: str,
    dialect: str,
    timeout_seconds: int = 3,
    max_rows: int = 10,
) -> dict:
    """Execute a query in an isolated sandbox. Tries PostgreSQL first, falls back to SQLite."""
    loop = asyncio.get_event_loop()

    # Try PostgreSQL if configured
    if settings.sandbox_database_url and _pg_available():
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    execute_query_pg_sync,
                    query,
                    dataset,
                    dialect,
                    timeout_seconds,
                    max_rows,
                ),
                timeout=timeout_seconds + 2,  # Extra buffer for schema setup
            )
            return result
        except Exception:
            pass  # Fall through to SQLite

    # Fallback to SQLite
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(
                None, execute_query_sync, query, dataset, dialect, timeout_seconds, max_rows
            ),
            timeout=timeout_seconds,
        )
        return result
    except asyncio.TimeoutError:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "execution_time_ms": timeout_seconds * 1000,
            "error": f"Query timed out after {timeout_seconds} seconds",
        }


def normalize_results(columns: list[str], rows: list[list]) -> list[list]:
    """Normalize query results for comparison."""
    normalized = []
    for row in rows:
        normalized_row = []
        for val in row:
            if val is None:
                normalized_row.append(None)
            elif isinstance(val, str):
                normalized_row.append(val.lower().strip())
            elif isinstance(val, float):
                normalized_row.append(round(val, 2))
            else:
                normalized_row.append(val)
        normalized.append(normalized_row)
    return sorted(normalized, key=lambda r: [str(v) for v in r])


def compare_results(
    user_columns: list[str],
    user_rows: list[list],
    expected_columns: list[str],
    expected_rows: list[list],
) -> dict:
    """Compare user query results against expected results."""
    # Normalize column names for comparison
    user_cols_norm = [c.lower().strip() for c in user_columns]
    expected_cols_norm = [c.lower().strip() for c in expected_columns]

    user_norm = normalize_results(user_columns, user_rows)
    expected_norm = normalize_results(expected_columns, expected_rows)

    mismatched_rows = []
    mismatched_columns = set()

    max_len = max(len(user_norm), len(expected_norm), 1)
    for i in range(max_len):
        if i >= len(user_norm) or i >= len(expected_norm):
            mismatched_rows.append(i)
            continue
        if user_norm[i] != expected_norm[i]:
            mismatched_rows.append(i)
            for j in range(min(len(user_norm[i]), len(expected_norm[i]))):
                if user_norm[i][j] != expected_norm[i][j] and j < len(expected_columns):
                    mismatched_columns.add(expected_columns[j])

    return {
        "matching_rows": max_len - len(mismatched_rows),
        "total_expected_rows": len(expected_norm),
        "mismatched_rows": mismatched_rows,
        "mismatched_columns": list(mismatched_columns),
        "is_correct": len(mismatched_rows) == 0 and user_cols_norm == expected_cols_norm,
    }
