from fastapi import FastAPI

from app.core.config import settings
from app.core.database import init_db
from app.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.include_router(api_router)

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    init_db(app)
    return app


app = create_app()
