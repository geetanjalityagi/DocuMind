from pydantic import BaseModel
from typing import List

class QuizRequest(BaseModel):
    document_id : str
    difficulty : str
    number_of_questions : int


class QuestionSchema(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    topic: str


class QuizResponse(BaseModel):
    questions: List[QuestionSchema]
