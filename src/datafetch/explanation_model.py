# This is the model where the AI would make the explantion in.

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from .exam_model import Exam, Image

class Mnemonic(BaseModel):
    tool: str = Field(..., description="The acronym, rhyme, or memory trick.")
    application: str = Field(..., description="How to apply this trick to the specific concept.")

    

class Lesson(BaseModel):
    topic_title: str = Field(..., description="A concise title for the lesson.")
    core_explanation: str = Field(..., description="A detailed breakdown of the logic and why the correct answer is right.")
    historical_context: str = Field(..., description="The background, origin, or 'story' behind this concept.")
    memory_aids: List[Mnemonic] = Field(..., description="A list of mnemonics to help retention.")
    similar_exam: Exam = Field(..., description="A follow-up mini-exam with new questions to test the concepts just taught.")
    images: List[Image] = Field(..., description="Images associated with the lesson. Remember to use the same name as the given data.")
    saved: Optional[bool]
    
    def add_images(self, images: Dict[str, Image]):
        for image in self.images:
            if image.name in images.keys():
                image.data = images[image.name].data
            else:
                print("cannot find image", image.name)