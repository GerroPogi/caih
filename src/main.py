# marker_single assets/language-profeciency-example.pdf --output_format json --ollama_base_url http://localhost:11434 --ollama_model gemini-3-flash-preview:cloud --llm_service=marker.services.ollama.OllamaService --output_dir language-profeciency-example.md --force_ocr --debug --disable_image_extraction

from datafetch import DataFetcher
from utils.timer import Timer
from utils.initiate_exam import initate_exam
import streamlit as st, os

st.set_page_config(
    page_title="Exam Generator"
)


st.title("Welcome to the Exam Generator!")
st.write("Click the button below to generate a new exam.")
start = st.button("Generate Exam")
st.session_state.subject = st.selectbox("Select what type of exam you want to generate", options=[subject.capitalize() for subject in [ subject for subject in os.listdir("assets") if os.path.isdir(os.path.join("assets", subject)) ]])
question_amount = st.slider("Select number of questions for the exam", min_value=1, max_value=100, value=10, step=1)
time_amount = st.slider("Set time limit for the exam (mins)", min_value=1, max_value=100, value=10, step=1)
st.session_state.data = DataFetcher()
datafetcher=st.session_state.data

st.write("## Pick your latest lessons")
with st.container(horizontal_alignment="left",border=True):
    for i, lesson in enumerate(datafetcher.get_lessons()[::-1]):
        if st.button(f"{i+1}. {lesson[:-7]}", args=[lesson]):
    
            st.session_state.lesson = datafetcher.get_lesson(lesson)
            st.switch_page("pages/lesson.py")
        



if start:
    st.cache_resource.clear()
    st.session_state.question_amount=question_amount
    st.session_state.time_amount= time_amount*60 # Converts into seconds
    initate_exam()
    
    st.switch_page("pages/exam.py")

