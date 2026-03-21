"""
Finance Dataset Package

Provides schema and seed SQL for a banking/finance database with 7 tables
and ~4000 rows of realistic data including intentional data quality
issues for the Data Debugging mode.
"""

from pathlib import Path

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_schema_sql() -> str:
    """Return the CREATE TABLE SQL statements for the finance schema."""
    return _SCHEMA_PATH.read_text(encoding="utf-8")


def get_seed_sql() -> str:
    """
    Generate and return INSERT SQL statements for all finance seed data.

    Uses random.Random(42) for reproducible output. Includes intentional
    data quality issues:
      - ~5% NULLs in phone fields
      - ~15 duplicate customer emails for debugging
      - Date gaps in transaction history (missing days)
      - Some transactions with incorrect balance_after values
    """
    from .seed import generate_seed_sql
    return generate_seed_sql()
