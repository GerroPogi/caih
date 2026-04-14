import json, os, re
from random import choice, randint
from ollama import Client
from .exam_model import Exam
from math import ceil

def load_exam(file_path="assets",subject=""):
    path=os.path.join(file_path, subject.lower())
    # Ensure directory exists to avoid infinite loops
    if not os.path.exists(path):
        os.makedirs(path)

    files = [f for f in os.listdir(path) if f.endswith(".json")]
    if not files:
        raise FileNotFoundError(f"No .json files found in {path}")
    
    file = choice(files) # Picks a random json file
    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_cuts(questions)-> list[int]:
    """
    Returns a list of random numbers that add up to the number of questions
    """
    cuts:list[int] = []
    max_cuts = ceil(questions / 3) # Cut into three parts
    while sum(cuts) < questions:
        cut = randint(1, max_cuts)
        cuts.append(cut)
    return cuts

def get_exam_from_ai(questions, subject):
    client = Client()
    cuts = get_random_cuts(questions)
    example_json = []
    image_list = [] # used for giving the AI the image
    formatted_images={} # Used to retrieve the image by assigning names
    for cut in cuts:
        exam_json=load_exam(subject=subject)
        start_number = randint(0, len(exam_json)-cut-1)
        exam = exam_json[start_number:start_number+cut]
        if any("images" in question for question in exam): # Imports the image if it exists and removes it to save space
            for question in exam:
                if question.get("images",[]):
                    images:dict =question.get("images")
                    question["images"] = images.keys()
                    image_list.extend(images)
                    for image_name, image in zip(images,question.get("images")):
                        formatted_images[image_name]=image
        example_json.extend(exam)
    # We only need a slice for context
    print(example_json)

    messages = [
        {
            'role': 'system', 
            'content': (
                "You are a pedagogical assistant that generates structured exam data. "
                "Your output must be a single, valid JSON object strictly following the provided schema. "
                "Do not include markdown formatting, backticks (```json), or any text outside the JSON structure. "
                "Ensure all internal string newlines are escaped as '\\n'."
            )
        },
        {
            'role': 'user',
            'content': (
                f"Generate an 'Exam' object containing {questions} new questions. "
                f"\n\n### SCHEMA CONSTRAINTS:\n{Exam.model_json_schema()}"
                f"\n\n### REFERENCE EXAMPLE:\n{json.dumps(example_json)}" # FIXME: Problem with Json things
                "\n\n### STRICT RULES:"
                "\n1. The 'id' must start at 1 and increment sequentially."
                "\n2. 'correct_answer' must be the choice id of the correc answer."
                "\n3. Map descriptions to the provided images accurately."
                "\n4. Return ONLY the raw JSON."
            ),
            "images": image_list  # Ensure your Ollama client supports the 'images' key here
        },
    ] # Thanks Gemini.
    while True: # Infinite Loop in case AI make mistakes
        final_exam = None
        # Using Gemini 3 Flash for high reliability
        try:
            response = client.chat(
                'gemini-3-flash-preview:latest', 
                messages=messages, 
                stream=False,
                format=Exam.model_json_schema(),
                )
            raw_content = response.message.content
            final_exam = Exam.model_validate_json(raw_content)
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            final_exam = None
        if final_exam:
            break
    
    return final_exam

def explain_exam(exam): # Deprecated for now
    client = Client()
    messages = [
        {
            'role': 'user',
            'content': f'Provide a clear, educational explanation for these questions. Focus on the logic behind the correct answers: {json.dumps(exam)}',
        },
    ]
    # OSS is fine for prose/explanations
    response = client.chat('gpt-oss:120b-cloud', messages=messages, stream=False)
    return response.message.content.strip()

if __name__ == "__main__":
    # Test the AI generation
    try:
        new_exam = get_exam_from_ai(questions=5,subject="mathematics")
        print(f"Successfully generated {len(new_exam)} questions.")
        print(json.dumps(new_exam[0], indent=2))
    except Exception as e:
        print(f"Error: {e}")