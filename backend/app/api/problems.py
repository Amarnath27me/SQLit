from fastapi import APIRouter, HTTPException

from app.services.problem_service import get_all_problems, get_problem_solution

router = APIRouter()

# Fields safe to expose in list view (no solution_query)
LIST_FIELDS = [
    "id", "slug", "title", "difficulty", "category", "dataset",
    "description", "schema_hint", "concept_tags", "hints",
    "explanation", "approach", "common_mistakes",
]


@router.get("")
@router.get("/")
async def list_problems(
    dataset: str | None = None,
    difficulty: str | None = None,
    category: str | None = None,
):
    problems = get_all_problems(dataset=dataset, difficulty=difficulty, category=category)
    total = len(problems)
    safe = [{k: p[k] for k in LIST_FIELDS if k in p} for p in problems]
    return {"problems": safe, "total": total}


@router.get("/{slug}")
async def get_problem(slug: str):
    problem = get_problem_solution(slug)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    # Never expose solution_query to frontend
    safe = {k: v for k, v in problem.items() if k != "solution_query"}
    return safe
