from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id : str
    document_id : str
    question : str