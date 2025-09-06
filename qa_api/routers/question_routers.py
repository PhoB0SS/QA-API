"""Question router"""

from typing import List, Tuple

from fastapi import APIRouter, status, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from qa_api.database.models import Question, Answer
from qa_api.response_models.models import QuestionResponse, AnswerResponse, QuestionCreate
from qa_api.database.engine import db_engine
from qa_api.routers.common_funcs.records_funcs import delete_record, create_record

router = APIRouter(prefix="/questions")


@router.get(path="/", status_code=status.HTTP_200_OK, response_model=List[QuestionResponse])
async def get_all_questions(session: AsyncSession = Depends(db_engine.get_async_session)) -> List[QuestionResponse]:
    """Transfers a list of all questions from the database"""

    stmt = select(Question)
    records = (await session.scalars(stmt)).all()

    if not records:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Questions not found")

    return [QuestionResponse.model_validate(record) for record in records]


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=str)
async def create_question(question: QuestionCreate, session: AsyncSession = Depends(db_engine.get_async_session)) -> str:
    """Create question in the database"""

    if not question.text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Text can not be empty")
    new_question = Question(text=question.text)
    return await create_record(new_question, session)


@router.get(path="/{id}", status_code=status.HTTP_200_OK, response_model=Tuple[QuestionResponse, List[AnswerResponse]])
async def get_all_answers(question_id: int = Path(..., alias="id"), session: AsyncSession = Depends(db_engine.get_async_session)) -> Tuple[QuestionResponse, List[AnswerResponse]]:
    """Transfers a list of all answers to question from the database"""

    question_stmt = select(Question).where(Question.id == question_id)

    question = await session.scalar(question_stmt)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question is not exists")

    answers_stmt = select(Answer).where(Answer.question_id == question.id)
    answers = await session.scalars(answers_stmt)

    return QuestionResponse.model_validate(question), [AnswerResponse.model_validate(answer) for answer in answers]


@router.delete(path="/{id}", status_code=status.HTTP_200_OK, response_model=str)
async def delete_question(question_id: int = Path(..., alias="id"), session: AsyncSession = Depends(db_engine.get_async_session)) -> str:
    """Delete question from the database"""

    return await delete_record(Question, question_id, session)
