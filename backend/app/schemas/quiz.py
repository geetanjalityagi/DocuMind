from pydantic import BaseModel, Field
from typing import List, Literal

class QuizRequest(BaseModel):
    document_id : str
    difficulty : str
    generation_mode: Literal["full_document", "topic"] = "full_document"
    topic: str | None = None
    num_questions: int = Field(default=10, ge=1, le=30)


class QuestionSchema(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    topic: str


class QuizResponse(BaseModel):
    questions: List[QuestionSchema]
