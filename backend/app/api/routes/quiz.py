from fastapi import APIRouter, HTTPException

from app.schemas.quiz import QuizRequest, QuizResponse
from app.services.quiz_service import generate_quiz

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)

@router.post("/", response_model=QuizResponse)
async def quiz(request : QuizRequest):
    try:
        answer = generate_quiz(request.document_id,
                      request.difficulty,
                      request.generation_mode,
                      request.topic,
                      request.num_questions
                )

        return answer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

