from fastapi import FastAPI

from ..storage.db_init import init_db
from .routes.history import router as history_router
from .routes.roll import router as roll_router
from .routes.sessions import router as sessions_router
from .routes.stats import router as stats_router


def create_app() -> FastAPI:
    init_db()

    app = FastAPI(title="Dice Game API", version="2.0.0")

    app.include_router(sessions_router)
    app.include_router(roll_router)
    app.include_router(history_router)
    app.include_router(stats_router)

    return app


app = create_app()
