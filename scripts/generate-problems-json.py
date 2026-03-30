"""
Generate a static JSON file of all problems for the frontend.

This embeds problem data at build time so the practice arena, interview,
and profile pages work without a live backend. Only query execution
still requires the backend.

Usage:
    python scripts/generate-problems-json.py
"""

import json
import sys
import os

# Add backend to path so we can import the problem service
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.problem_service import get_all_problems

# Fields safe to expose (no solution_query)
LIST_FIELDS = [
    "id", "slug", "title", "difficulty", "category", "dataset",
    "description", "schema_hint", "concept_tags", "hints",
    "explanation", "approach", "common_mistakes",
]

def main():
    problems = get_all_problems()
    safe = [{k: p[k] for k in LIST_FIELDS if k in p} for p in problems]

    out_path = os.path.join(
        os.path.dirname(__file__), "..", "frontend", "src", "data", "problems.json"
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"problems": safe, "total": len(safe)}, f, ensure_ascii=False)

    print(f"Generated {len(safe)} problems -> {os.path.abspath(out_path)}")

if __name__ == "__main__":
    main()
