import streamlit as st
import json
from datafetch.exam_model import Exam
from utils.initiate_exam import initate_exam
from datafetch.exam_model import Exam

def format_tabs(text:str, tab_amount:int = 8):
    return f"{"&nbsp;"*tab_amount}{("&nbsp;"*8).join(text.split("\n"))}"

lesson = st.session_state.lesson 

st.title(lesson.topic_title)
# st.write("First column&nbsp;&nbsp;&nbsp;&nbsp;Second column")

core_explanations_tab, historical_context_tab, memory_aids_tab = st.tabs(["Core Explanations", "Historical Context", "Memory Aids"])

with core_explanations_tab:
    st.write(f"{"&nbsp;"*8}{lesson.core_explanation}")

with historical_context_tab:
    st.write(f"{"&nbsp;"*8}{lesson.historical_context}")

with memory_aids_tab:
    memory_aids = lesson.memory_aids
    for mnemonic in memory_aids:
        st.write(f"**{mnemonic.tool}**: {mnemonic.application}")

st.write("---")

col1, col2, col3 = st.columns(3)
with col1:
    try_exam = st.button("Try the Exam") # TODO: add functionality to this
with col2:
    if not lesson.saved:
        if st.button("Save Lesson"):
            st.session_state.data.save_lesson(lesson, lesson.topic_title) # TODO: Check if this worksst.button("Save Lesson")

with col3:
    go_home = st.button("Go Home")



if go_home:
    st.switch_page("main.py")

if try_exam:
    initate_exam()
    st.session_state.exam=lesson.similar_exam
    st.switch_page("pages/exam.py")
