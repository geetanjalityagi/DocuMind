from fastapi import APIRouter, HTTPException

from app.services.notes_service import generate_notes

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.post("/{document_id}")
async def notes(document_id : str):

    try:
        notes = generate_notes(document_id)

        return {
            "document_id": document_id,
            "notes": notes,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )