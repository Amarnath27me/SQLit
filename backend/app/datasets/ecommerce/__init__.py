"""
E-Commerce Dataset Package

Provides schema and seed SQL for an e-commerce database with 8 tables
and ~4500 rows of realistic data including intentional data quality
issues for the Data Debugging mode.
"""

from pathlib import Path

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_schema_sql() -> str:
    """Return the CREATE TABLE SQL statements for the e-commerce schema."""
    return _SCHEMA_PATH.read_text(encoding="utf-8")


def get_seed_sql() -> str:
    """
    Generate and return INSERT SQL statements for all e-commerce seed data.

    Uses Faker with seed(42) for reproducible output. Includes intentional
    data quality issues:
      - ~5% NULLs in phone, comment, and delivery_date fields
      - ~20 duplicate customer emails
      - ~50 orders with mismatched total_amount vs sum of order_items
      - Date gaps in order history (missing days)
    """
    from .seed import generate_seed_sql
    return generate_seed_sql()
