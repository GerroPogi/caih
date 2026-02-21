# This is where they can grab data for prompting.

import json,os
from random import choice

def load_exam(file_path="assets"):
    file_path = os.path.join(file_path)
    while True:
        file = choice(os.listdir(file_path))
        if file.endswith(".json"):
            break
    
    with open(os.path.join(file_path, file), "r") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    print(load_exam()[0])