
from .prompting import get_exam_from_ai, explain_exam

class DataFetcher:
    def __init__(self):
        pass

    def fetch_exam(self):
        return get_exam_from_ai()

    def fetch_explanation(self, exam):
        return explain_exam(exam)