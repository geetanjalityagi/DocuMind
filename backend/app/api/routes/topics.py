from fastapi import APIRouter, HTTPException

from app.services.topic_service import extract_topics

router = APIRouter(
    prefix="/topics",
    tags=['Topics']
)

@router.post("/{document_id}")
async def topics(document_id : str):

    try:
        topics = extract_topics(document_id)

        return {
            "document_id": document_id,
            "topics": topics,
            "total_topics": len(topics),
            "status": "success"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))