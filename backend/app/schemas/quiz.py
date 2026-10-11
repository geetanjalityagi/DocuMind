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
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: Literal["A", "B", "C", "D"]
    topic: str


class QuizResponse(BaseModel):
    questions: List[QuestionSchema]
