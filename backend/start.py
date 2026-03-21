"""Entrypoint script — reads PORT from environment and starts uvicorn."""
import os
import uvicorn

port = int(os.environ.get("PORT", "8001"))
print(f"Starting SQLit API on port {port}")

uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=port,
    workers=int(os.environ.get("WEB_WORKERS", "1")),
    log_level="info",
)
