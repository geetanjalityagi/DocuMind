from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest
from app.services.rag_services import rag_pipeline

router = APIRouter(
    prefix="/chats",
    tags=["Chats"]
)

@router.post("/chat")
async def chat(request : ChatRequest):
    try:

        answer = rag_pipeline(
            session_id=request.session_id,
            document_id=request.document_id,
            input=request.question
        )

        return {
            "session_id": request.session_id,
            "document_id": request.document_id,
            "question": request.question,
            "answer": answer
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )