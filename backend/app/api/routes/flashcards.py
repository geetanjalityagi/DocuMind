from fastapi import APIRouter, HTTPException

from app.schemas.flashcards import FlashCardRequest, FlashCardResponse
from app.services.flashcard_service import generate_flashcards

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)

@router.post("/", response_model=FlashCardResponse)
async def quiz(request : FlashCardRequest):
    try:
        answer = generate_flashcards(request.document_id,
                      request.generation_mode,
                      request.topic,
                      request.num_flashcards
                )

        return answer

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

