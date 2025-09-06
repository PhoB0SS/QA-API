"""Answer router"""

from fastapi import APIRouter, status, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from qa_api.database.models import Answer
from qa_api.database.engine import db_engine
from qa_api.response_models.models import AnswerResponse, AnswerCreate
from qa_api.routers.common_funcs.records_funcs import delete_record, create_record

router = APIRouter()


@router.post("/questions/{id}/answers/", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_answer(answer: AnswerCreate, session: AsyncSession = Depends(db_engine.get_async_session)) -> str:
    """Create answer for question"""

    if not answer.text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Text can not be empty")
    new_answer = Answer(question_id=answer.question_id, user_id=str(answer.user_id), text=answer.text)
    return await create_record(new_answer, session)


@router.get("/answers/{id}", status_code=status.HTTP_200_OK, response_model=AnswerResponse)
async def get_answer(answer_id: int = Path(..., alias="id"), session: AsyncSession = Depends(db_engine.get_async_session)) -> AnswerResponse:
    """Get answer by its id"""

    stmt = select(Answer).where(Answer.id == answer_id)
    result = await session.scalar(stmt)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Answer is not exists")

    return AnswerResponse.model_validate(result)

@router.delete("/answers/{id}", status_code=status.HTTP_200_OK, response_model=str)
async def delete_answer(answer_id: int = Path(..., alias="id"), session: AsyncSession = Depends(db_engine.get_async_session)) -> str:
    """Delete answer by its id"""

    return await delete_record(Answer, answer_id, session)