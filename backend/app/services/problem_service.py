"""
Problem service — loads problems from all dataset modules and provides lookup.
"""

import logging

logger = logging.getLogger(__name__)

_problems_cache: dict[str, dict] = {}

# All dataset modules to load
DATASET_MODULES = [
    "app.datasets.ecommerce.problems",
    "app.datasets.finance.problems",
    "app.datasets.healthcare.problems",
]

# Normalize inconsistent category names to canonical kebab-case values
_CATEGORY_MAP: dict[str, str] = {
    # Healthcare snake_case variants
    "group_by": "aggregation",
    "aggregate": "aggregation",
    "having": "aggregation",
    "join": "joins",
    "left_join": "joins",
    "self_join": "joins",
    "window_function": "window-functions",
    "date_functions": "advanced",
    "set_operations": "advanced",
    "functions": "advanced",
    "division": "advanced",
    "case": "advanced",
    "subquery": "subqueries",
    # Healthcare interview ALL CAPS variants
    "GROUP BY": "aggregation",
    "WHERE": "where",
    "ORDER BY": "select",
    "JOIN": "joins",
    "CTE": "cte",
    "window functions": "window-functions",
    "HAVING": "aggregation",
    # Finance interview freeform variants
    "filtering": "where",
    "string filtering": "where",
    "sorting and limiting": "select",
    "joins and aggregation": "joins",
    "conditional aggregation": "aggregation",
    "correlated subquery": "subqueries",
    "fraud detection": "advanced",
    "cohort analysis": "advanced",
    "date arithmetic": "advanced",
    "recursive cte": "cte",
    "data cleaning": "advanced",
    # Ecommerce interview "Interview — X" variants (strip prefix)
    "Interview — Aggregation": "aggregation",
    "Interview — NULL Handling": "advanced",
    "Interview — UNION": "advanced",
    "Interview — Subqueries": "subqueries",
    "Interview — Window Functions": "window-functions",
    "Interview — CTE": "cte",
    "Interview — Joins": "joins",
}


def _normalize_category(category: str) -> str:
    """Normalize category to one of: select, where, aggregation, joins, subqueries, window-functions, cte, advanced."""
    if category in _CATEGORY_MAP:
        return _CATEGORY_MAP[category]
    # Strip "Interview — " prefix for any not explicitly mapped
    if category.startswith("Interview — "):
        base = category[len("Interview — "):].lower().strip()
        for canonical in ("select", "where", "aggregation", "joins", "subqueries", "window-functions", "cte", "advanced"):
            if canonical in base or base in canonical:
                return canonical
        return "advanced"
    # Already canonical
    return category


def _load_problems():
    """Load all problems from dataset modules."""
    global _problems_cache
    if _problems_cache:
        return

    for module_path in DATASET_MODULES:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            for p in mod.PROBLEMS:
                # Normalize category at load time
                p["category"] = _normalize_category(p.get("category", "advanced"))
                _problems_cache[p["id"]] = p
                _problems_cache[p["slug"]] = p
        except (ImportError, AttributeError) as e:
            logger.warning("Failed to load dataset module %s: %s", module_path, e)


def get_problem_solution(problem_id: str) -> dict | None:
    """Get a problem by ID or slug."""
    _load_problems()
    return _problems_cache.get(problem_id)


def get_all_problems(
    dataset: str | None = None,
    difficulty: str | None = None,
    category: str | None = None,
) -> list[dict]:
    """Get filtered list of problems."""
    _load_problems()

    # Deduplicate (problems are stored by both id and slug)
    seen = set()
    problems = []
    for p in _problems_cache.values():
        if p["id"] in seen:
            continue
        seen.add(p["id"])

        if dataset and p.get("dataset") != dataset:
            continue
        if difficulty and p.get("difficulty") != difficulty:
            continue
        if category and p.get("category") != category:
            continue

        problems.append(p)

    # Sort by dataset then by id for consistent ordering
    problems.sort(key=lambda p: (p.get("dataset", ""), p.get("id", "")))
    return problems
