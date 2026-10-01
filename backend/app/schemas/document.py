from pydantic import BaseModel

class DocumentResponse(BaseModel):
    document_id : str
    filename : str
    file_size : int
    title : str
    chunks_size : int
    status : str