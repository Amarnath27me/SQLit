from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.security import validate_query
from app.core.rate_limiter import query_rate_limiter
from app.services.query_executor import (
    execute_sandboxed_query,
    compare_results,
)
from app.services.problem_service import get_problem_solution

router = APIRouter()

XP_REWARDS = {"easy": 10, "medium": 25, "hard": 50}


class QueryRequest(BaseModel):
    query: str
    problem_id: str | None = None
    dialect: str = "postgresql"
    dataset: str = "ecommerce"


class QueryResultData(BaseModel):
    columns: list[str] = []
    rows: list[list] = []
    row_count: int = 0
    execution_time_ms: float = 0


class DiffData(BaseModel):
    matching_rows: int = 0
    total_expected_rows: int = 0
    mismatched_rows: list[int] = []
    mismatched_columns: list[str] = []


class QueryResponse(BaseModel):
    status: str  # "accepted" | "wrong_answer" | "error"
    user_result: QueryResultData | None = None
    expected_result: QueryResultData | None = None
    diff: DiffData | None = None
    error: str | None = None
    xp_earned: int = 0


@router.post("/execute", response_model=QueryResponse)
async def execute_query(req: QueryRequest, request: Request):
    # Rate limit by IP
    client_ip = request.client.host if request.client else "unknown"
    if not query_rate_limiter.is_allowed(client_ip):
        remaining = query_rate_limiter.remaining(client_ip)
        return QueryResponse(
            status="error",
            error=f"Rate limit exceeded. Max 20 queries per minute. Try again shortly.",
        )

    # Validate query
    is_valid, error = validate_query(req.query)
    if not is_valid:
        return QueryResponse(status="error", error=error)

    # Execute user query
    user_result = await execute_sandboxed_query(
        query=req.query,
        dataset=req.dataset,
        dialect=req.dialect,
    )

    if not user_result["success"]:
        return QueryResponse(
            status="error",
            error=user_result.get("error", "Query execution failed"),
            user_result=QueryResultData(
                execution_time_ms=user_result["execution_time_ms"]
            ),
        )

    # Sandbox mode — no problem_id, just return the result
    if not req.problem_id:
        return QueryResponse(
            status="accepted",
            user_result=QueryResultData(
                columns=user_result["columns"],
                rows=user_result["rows"],
                row_count=user_result["row_count"],
                execution_time_ms=user_result["execution_time_ms"],
            ),
        )

    # Practice mode — compare against expected solution
    problem = get_problem_solution(req.problem_id)
    if not problem:
        return QueryResponse(status="error", error="Problem not found")

    # Execute expected solution
    expected_result = await execute_sandboxed_query(
        query=problem["solution_query"],
        dataset=req.dataset,
        dialect=req.dialect,
    )

    if not expected_result["success"]:
        return QueryResponse(
            status="error",
            error="Internal error: solution query failed",
            user_result=QueryResultData(
                columns=user_result["columns"],
                rows=user_result["rows"],
                row_count=user_result["row_count"],
                execution_time_ms=user_result["execution_time_ms"],
            ),
        )

    # Compare results
    diff = compare_results(
        user_columns=user_result["columns"],
        user_rows=user_result["rows"],
        expected_columns=expected_result["columns"],
        expected_rows=expected_result["rows"],
    )

    is_correct = diff["is_correct"]
    xp = XP_REWARDS.get(problem.get("difficulty", "easy"), 10) if is_correct else 0

    return QueryResponse(
        status="accepted" if is_correct else "wrong_answer",
        user_result=QueryResultData(
            columns=user_result["columns"],
            rows=user_result["rows"],
            row_count=user_result["row_count"],
            execution_time_ms=user_result["execution_time_ms"],
        ),
        expected_result=QueryResultData(
            columns=expected_result["columns"],
            rows=expected_result["rows"],
            row_count=expected_result["row_count"],
            execution_time_ms=expected_result["execution_time_ms"],
        ) if not is_correct else None,
        diff=DiffData(**diff) if not is_correct else None,
        error=None,
        xp_earned=xp,
    )
