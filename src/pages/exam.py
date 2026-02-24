import streamlit as st

st.title("Exam Page")

@st.cache_data
def get_exam():
    return st.session_state.data.fetch_exam()

st.write(get_exam())
if st.button("Go back"):
    st.switch_page("main.py")