# Pydantic Model of what the AI must follow
from pydantic import BaseModel
from typing import List

class Image(BaseModel):
    description: str
    image_name: str

class Question(BaseModel):
    id: str
    question: str
    choices: List[str]
    images: List[Image]
    correct_answer: int
    explanation: str


class QuestionList(BaseModel):
    questions: List[Question]
    instruction: str

class Exam(BaseModel):
    types: List[QuestionList]