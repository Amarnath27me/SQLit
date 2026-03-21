from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sqlit"
    sandbox_database_url: str = "postgresql://postgres:postgres@localhost:5432/sqlit_sandbox"

    # Auth0
    auth0_domain: str = ""
    auth0_api_audience: str = ""
    auth0_algorithms: list[str] = ["RS256"]

    # Auth0 — CAPTCHA (Bot Detection) should be enabled in the Auth0 dashboard:
    # Dashboard → Security → Bot Detection → Enable for signup/login flows

    # CORS — comma-separated in env: CORS_ORIGINS=https://sqlit.dev,http://localhost:3000
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://sqlit.dev",
        "https://www.sqlit.dev",
    ]

    # Query execution
    query_timeout_seconds: int = 3
    max_result_rows: int = 1000
    rate_limit_per_minute: int = 20

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
