"""FastAPI app"""

from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from qa_api.routers import answer_routers, question_routers
from qa_api.database.engine import db_engine
from qa_api.logger.logger import logger


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, Any]:
    """Lifespan of the app"""

    await db_engine.check_database()
    logger.info("App started")
    yield
    logger.info("App closed")
    await db_engine.dispose()

app = FastAPI(title="Q-A API", lifespan=lifespan)
app.include_router(answer_routers.router, tags=["answers"])
app.include_router(question_routers.router, tags=["questions"])
