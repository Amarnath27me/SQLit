import json
from pydantic_settings import BaseSettings


def _parse_origins(raw: str) -> list[str]:
    """Parse CORS origins from any format: JSON array, comma-separated, or single URL."""
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("["):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    return [o.strip() for o in raw.split(",") if o.strip()]


_DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://sqlit.dev",
    "https://www.sqlit.dev",
]


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sqlit"
    sandbox_database_url: str = "postgresql://postgres:postgres@localhost:5432/sqlit_sandbox"

    # Auth0
    auth0_domain: str = ""
    auth0_api_audience: str = ""
    auth0_algorithms: str = '["RS256"]'

    # CORS — accepts any format in env:
    #   CORS_ORIGINS=https://sqlit.dev,http://localhost:3000
    #   CORS_ORIGINS=["https://sqlit.dev","http://localhost:3000"]
    cors_origins: str = ""

    # Query execution
    query_timeout_seconds: int = 3
    max_result_rows: int = 1000
    rate_limit_per_minute: int = 20

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.cors_origins:
            return _DEFAULT_ORIGINS
        return _parse_origins(self.cors_origins)

    @property
    def auth0_algorithms_list(self) -> list[str]:
        return json.loads(self.auth0_algorithms)

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
