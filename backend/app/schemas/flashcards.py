from pydantic import BaseModel, Field
from typing import Literal, List

class FlashCardRequest(BaseModel):
    document_id : str
    generation_mode: Literal["full_document", "topic"] = "full_document"
    topic: str | None = None
    num_flashcards: int

class QuestionSchema(BaseModel):
    question: str
    answer : str
    topic: str


class FlashCardResponse(BaseModel):
    questions: List[QuestionSchema]