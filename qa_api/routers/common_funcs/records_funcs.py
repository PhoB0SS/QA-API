"""Common functions for routers"""

from typing import Type

from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from qa_api.database.models import Base
from qa_api.logger.logger import logger


async def delete_record(model: Type[Base], record_id: int, session: AsyncSession) -> str:
    """Delete record from database"""

    record = await session.get(model, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} is not exists")
    await session.delete(record)
    await session.commit()
    logger.info(f"Record deleted: {record}")

    return f"{model.__name__} deleted successfully."


async def create_record(instance: Base, session: AsyncSession) -> str:
    """Create record in database"""

    try:
        session.add(instance)
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Integrity error occurred: {e.orig}")
    logger.info(f"Created new record: {instance}")

    return f"{type(instance).__name__} created"