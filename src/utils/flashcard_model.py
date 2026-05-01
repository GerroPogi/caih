from typing import List, Optional

from pydantic import BaseModel

from datafetch.exam_model import Image


class Flashcard(BaseModel):
    question: str
    answer: str
    images: Optional[List[Image]] = None

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer


class FlashcardSet(BaseModel):
    topic: str
    flashcards: List[Flashcard]

    def get_topic(self):
        return self.topic

    def get_flashcards(self):
        return self.flashcards

    def add_flashcard(self, flashcard: Flashcard):
        self.flashcards.append(flashcard)
