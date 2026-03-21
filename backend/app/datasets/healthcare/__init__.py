"""
Healthcare Dataset Package

Provides schema and seed SQL for a healthcare database with 8 tables
and ~4000 rows of realistic data including intentional data quality
issues for the Data Debugging mode.
"""

from pathlib import Path

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_schema_sql() -> str:
    """Return the CREATE TABLE SQL statements for the healthcare schema."""
    return _SCHEMA_PATH.read_text(encoding="utf-8")


def get_seed_sql() -> str:
    """
    Generate and return INSERT SQL statements for all healthcare seed data.

    Uses random with seed(42) for reproducible output. Includes intentional
    data quality issues:
      - ~5% NULLs in phone fields
      - ~10 duplicate patient emails
      - Date gaps in visit history
      - Some overdue billing records with NULL paid_at
    """
    from .seed import generate_seed_sql
    return generate_seed_sql()
