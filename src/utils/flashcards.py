import json
import os
from typing import List

from datafetch.exam_model import Image
from utils.flashcard_model import Flashcard, FlashcardSet


def get_flashcards(topic):
    flashcards_dir = os.path.join("flashcards", topic)
    flashcards = FlashcardSet(topic=topic, flashcards=[])

    if not os.path.exists(flashcards_dir):
        os.makedirs(flashcards_dir)
        return flashcards

    for filename in os.listdir(flashcards_dir):
        if filename.endswith(".json"):
            with open(os.path.join(flashcards_dir, filename), "r") as f:
                content = f.read()
                flashcards.add_flashcard(Flashcard(**json.loads(content)))

    return flashcards


def get_flashcard_topics():
    flashcards_dir = os.path.join("flashcards")
    if not os.path.exists(flashcards_dir):
        return []
    return [
        d
        for d in os.listdir(flashcards_dir)
        if os.path.isdir(os.path.join(flashcards_dir, d))
    ]


def save_flashcard_to_flashcard(flashcard: Flashcard, topic: str):
    flashcards_dir = os.path.join("flashcards", topic)
    if not os.path.exists(flashcards_dir):
        os.makedirs(flashcards_dir)

    filename = f"{flashcard.question}.json"
    with open(os.path.join(flashcards_dir, filename), "w") as f:
        json.dump(flashcard.model_dump(), f)


def save_text_to_flashcard(question: str, answer: str, images: List[Image], topic: str):
    flashcards_dir = os.path.join("flashcards", topic)
    if not os.path.exists(flashcards_dir):
        os.makedirs(flashcards_dir)
    flashcard = Flashcard(question=question, answer=answer, images=images)
    filename = f"{flashcard.question}.json"
    with open(os.path.join(flashcards_dir, filename), "w") as f:
        json.dump(flashcard.model_dump(), f)
