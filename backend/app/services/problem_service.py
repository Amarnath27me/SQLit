"""
Problem service — loads problems from all dataset modules and provides lookup.
"""

_problems_cache: dict[str, dict] = {}

# All dataset modules to load
DATASET_MODULES = [
    "app.datasets.ecommerce.problems",
    "app.datasets.finance.problems",
    "app.datasets.healthcare.problems",
]


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
                _problems_cache[p["id"]] = p
                _problems_cache[p["slug"]] = p
        except (ImportError, AttributeError) as e:
            # Dataset not yet available — skip silently
            pass


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
