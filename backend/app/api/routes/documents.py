from fastapi import UploadFile, File, APIRouter, HTTPException
from app.schemas.document import DocumentResponse
from app.services.document_services import save_document
from app.schemas.document import DocumentResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    document_info = await save_document(file)

    return document_info