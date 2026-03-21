import re

# Blocked SQL keywords (case-insensitive)
BLOCKED_KEYWORDS = [
    "DROP", "DELETE", "ALTER", "CREATE", "INSERT", "UPDATE", "TRUNCATE",
    "COPY", "pg_sleep", "pg_catalog", "information_schema",
    "pg_stat", "pg_proc", "pg_class", "pg_namespace",
    "GRANT", "REVOKE", "EXECUTE", "CALL",
]

BLOCKED_PATTERN = re.compile(
    r"\b(" + "|".join(BLOCKED_KEYWORDS) + r")\b",
    re.IGNORECASE,
)

MULTI_STATEMENT_PATTERN = re.compile(r";\s*\S")

# Max query length (prevent extremely long queries)
MAX_QUERY_LENGTH = 5000


def validate_query(sql: str) -> tuple[bool, str | None]:
    """Validate a SQL query for safety. Returns (is_valid, error_message)."""
    stripped = sql.strip().rstrip(";")

    if not stripped:
        return False, "Empty query"

    if len(stripped) > MAX_QUERY_LENGTH:
        return False, f"Query too long. Maximum {MAX_QUERY_LENGTH} characters allowed."

    # Must start with SELECT or WITH (CTE)
    upper = stripped.upper().lstrip()
    if not (upper.startswith("SELECT") or upper.startswith("WITH")):
        return False, "Only SELECT statements are allowed (CTEs with WITH are also permitted)"

    # If starts with WITH, make sure it contains a SELECT
    if upper.startswith("WITH") and "SELECT" not in upper:
        return False, "CTE (WITH) must contain a SELECT statement"

    # Block dangerous keywords
    match = BLOCKED_PATTERN.search(stripped)
    if match:
        return False, f"Blocked keyword: {match.group()}"

    # Block multiple statements
    if MULTI_STATEMENT_PATTERN.search(stripped):
        return False, "Multiple statements are not allowed"

    # Block comment-based attacks
    if "--" in stripped or "/*" in stripped:
        return False, "SQL comments are not allowed"

    return True, None
