"""Engine for SQLAlchemy"""

import sys
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from config import DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME
from qa_api.logger.logger import logger


class DatabaseEngine:
    """Allow to interact with the database"""

    def __init__(self, db_url: str) -> None:
        """Initialize the database engine"""

        self._engine: AsyncEngine = create_async_engine(db_url, echo=True)
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(self._engine, expire_on_commit=False)
        logger.info('Database engine started')


    async def check_database(self) -> None:
        """Checking database availability when starting an application"""

        try:
            async with self._session_maker() as session:
                await session.execute(text("SELECT 1"))
            logger.info("Connection to database established successfully.")
        except SQLAlchemyError as err:
            logger.critical(f"Unable to connect to the database due to a SQLAlchemy error: {err}")
            sys.exit(1)

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Async session generator"""

        try:
            async with self._session_maker() as session:
                yield session
        except SQLAlchemyError as err:
            logger.error(f"Database session error: {err}", exc_info=True)
            sys.exit(1)

    async def dispose(self) -> None:
        """Close database connection"""

        await self._engine.dispose()


db_engine = DatabaseEngine(db_url=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
