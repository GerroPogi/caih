# marker_single assets/language-profeciency-example.pdf --output_format json --ollama_base_url http://localhost:11434 --ollama_model gemini-3-flash-preview:cloud --llm_service=marker.services.ollama.OllamaService --output_dir language-profeciency-example.md --force_ocr --debug --disable_image_extraction


from ollama import Client
from prompting.data import load_exam

client = Client()

exam = load_exam()

messages = [
  {
    'role': 'user',
    'content': 'Create 5 questions just like the following text: ' + str(exam[0:4]),
  },
]

messages = client.chat('gpt-oss:120b-cloud', messages=messages, stream=False)
print(messages.message.content, end='', flush=True)