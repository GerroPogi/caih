# Pydantic Model of what the AI must follow
from pydantic import BaseModel
from typing import List, Optional, Any

class Image(BaseModel):
    description: str
    data: Optional[bytes]
    name: str

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
    
    def add_images(self, images: dict):
        for image in self.images:
            if image.image_name in images.keys():
                image.data = images[image.image_name]
            else:
                print("cannot find image", image.image_name)
    
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
    def add_images(self, images: dict):
        for question in self.questions:
            question.add_images(images)
    
    def add_answer(self, question_id, answer):
        for question in self.questions:
            if question.id == question_id:
                question.add_answer(answer)
                break
        else:
            raise ValueError(f"Question with ID {question_id} not found")

class Exam(BaseModel):
    types: List[QuestionList]
    
    def add_images(self, images: dict):
        for question_list in self.types:
            question_list.add_images(images)