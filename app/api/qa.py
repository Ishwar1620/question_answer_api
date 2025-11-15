"""QA API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.qa import QuestionRequest, AnswerResponse
from app.services.qa_service import QAService
from database.db import get_db_session
from app.core.security import validate_question

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: QuestionRequest,
    db: AsyncSession = Depends(get_db_session)
) -> AnswerResponse:
    """Ask a question and get an answer."""
    try:
        # Validate question
        is_valid, error_message = validate_question(request.question)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Initialize service
        qa_service = QAService()
        
        # Get user ID if possible
        user_id = await qa_service.get_user_id(db, request.question)
        
        # Get answer
        result = await qa_service.get_answer(request.question, user_id)
        
        return AnswerResponse(
            answer=result.get("answer", "Answer cannot be determined.")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your question"
        )
