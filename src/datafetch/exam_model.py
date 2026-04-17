# Pydantic Model of what the AI must follow
from pydantic import BaseModel
from typing import List, Optional

class Image(BaseModel):
    description: str
    image_name: str

class Choice(BaseModel):
    choice: str
    id:str

class Question(BaseModel):
    id: str
    question: str
    choices: List[Choice]
    images: List[Image]
    correct_answer: str
    explanation: str
    answer: Optional[str] = None
    def add_answer(self,answer:str):
        self.answer = answer
    
    def get_choice(self, choice_id) -> Optional[Choice]:
        for choice in self.choices:
            if choice.id == choice_id:
                return choice
        return None



class QuestionList(BaseModel):
    questions: List[Question]
    instruction: str
    
    def delete_question(self, question_id):
        try:
            self.questions = [question for question in self.questions if question.id != question_id]
        except ValueError:
            pass
    
    def add_answer(self, question_id, answer):
        for question in self.questions:
            if question.id == question_id:
                question.add_answer(answer)
                break
        else:
            raise ValueError(f"Question with ID {question_id} not found")

class Exam(BaseModel):
    types: List[QuestionList]