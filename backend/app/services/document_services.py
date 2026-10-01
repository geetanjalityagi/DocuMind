from uuid import uuid4

from fastapi import UploadFile
from pypdf import PdfReader

from app.config import UPLOAD_DIR

from langchain_text_splitters import RecursiveCharacterTextSplitter


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


    documents = ""
    
    for page in reader.pages:
        page_content = page.extract_text()

        if page_content:
            documents += page_content + "\n"

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 250)
    chunks = text_splitter.split_text(documents)


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