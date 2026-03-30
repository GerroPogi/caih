import requests, time, json
from tkinter import Tk, filedialog
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("DATALABS_API_KEY")

url = "https://www.datalab.to/api/v1/convert"
headers = {"X-Api-Key": key}

def get_file_from_user():
    root = Tk()
    root.withdraw()
    # Bring the window to the front
    root.attributes('-topmost', True) 
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    root.destroy() # Properly close the tkinter instance
    if not file_path:
        return None
    return os.path.abspath(file_path) # Use absolute path

file_path = get_file_from_user()

if file_path:
    with open(file_path, "rb") as f:
        resp = requests.post(
            url,
            files={"file": (os.path.basename(file_path), f, "application/pdf")},
            headers=headers,
        )

    data = resp.json()
    print(json.dumps(data, indent=4))

    if "request_check_url" in data:
        check_url = data["request_check_url"]

        # Poll until complete
        for _ in range(300):
            r = requests.get(check_url, headers=headers).json()
            if r.get("status") == "complete":
                # Create output paths based on the original file location
                base_path = os.path.splitext(file_path)[0]
                
                with open(f"{base_path}.md", "w", encoding="utf-8") as f:
                    f.write(r.get("markdown", ""))
                
                with open(f"{base_path}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(r, indent=4))
                
                print(f"Success! Files saved to {base_path}")
                break
            print("Processing...")
            time.sleep(2)
    else:
        print("Error: No check URL returned from API.")