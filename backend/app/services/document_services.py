from uuid import uuid4

from fastapi import UploadFile
from pypdf import PdfReader

from app.config import UPLOAD_DIR

from langchain_core.documents import Document

from app.services.embedding_services import embed_text
from app.services.chunk_service import create_chunks


async def save_document(file: UploadFile):

    # Generate unique document ID
    document_id = str(uuid4())

    # Create PDF path
    file_path = UPLOAD_DIR / f"{document_id}.pdf"

    # Read uploaded file
    content = await file.read()

    # Save PDF
    file_path.write_bytes(content)

    try:
        # Read PDF information
        reader = PdfReader(str(file_path))

        page_count = len(reader.pages)

        metadata = reader.metadata

        title = (
            metadata.title
            if metadata and metadata.title
            else file.filename
        )

    except Exception:
        file_path.unlink(missing_ok=True)

        raise ValueError("Invalid or corrupted PDF")


    documents = []
    
    for page_no, page in enumerate(reader.pages, start=1):
        page_content = page.extract_text()

        if page_content:
            documents.append(
                Document(
                    page_content = page_content,
                    metadata={
                        "document_id" : document_id,
                        "file_name" : file.filename,
                        "page_no" : page_no
                    }
                )
            ) 

    chunks = create_chunks(documents)

    embed_text(chunks, document_id)

    return {
        "document_id": document_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
        "page_count": page_count,
        "title": title,
        "chunks_size": len(chunks),
        "status": "uploaded"
    }