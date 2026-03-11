from fastapi import FastAPI

from ..storage.sqlite_storage import init_db
from .routes.history import router as history_router
from .routes.roll import router as roll_router
from .routes.stats import router as stats_router

init_db()

app = FastAPI(title="Dice Game API", version="1.0.0")

app.include_router(roll_router)
app.include_router(history_router)
app.include_router(stats_router)
