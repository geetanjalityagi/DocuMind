from pydantic import BaseModel

class DocumentResponse(BaseModel):
    document_id : str
    filename : str
    content_type : str
    file_size : int
    page_count : int
    title : str
    chunks_size : int
    status : str
