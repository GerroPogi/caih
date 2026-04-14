import json

import streamlit as st

st.title("Exam Page")

def get_data(model,key): pass

@st.cache_data
def get_exam():
    print(st.session_state.data.fetch_exam)
    exam = st.session_state.data.fetch_exam(st.session_state.question_amount,st.session_state.subject)
    return exam


exam=get_exam()
st.session_state.exam=exam
# print(exam,"exam") # Only use for debugging 
# print(st.session_state.question_type,len(exam))

current_page_type = exam.types[min(st.session_state.question_type,len(exam.types)-1)]
# print(current_page_type)

CORRECT = 1
WRONG = 2
DISABLED = 3
def render_questions():
    exam_dict_key =current_page_type.instruction # Grabs the instructions
    st.write(exam_dict_key)
    for question in current_page_type.questions:
        st.markdown(f"{question.id}.  {question.question}", unsafe_allow_html=True)
        def on_choice_click(choice, question):
            correct_answer = question.correct_answer
            
            for disable_choice in question.choices:
                st.session_state[f"button_{question.id}{disable_choice.id.lower()}_value"] = DISABLED
            print(choice, "choice")
            if choice.id == correct_answer:
                st.session_state[f"button_{question.id}{choice.id.lower()}_value"] = CORRECT
                
            else:
                st.session_state[f"button_{question.id}{choice.id.lower()}_value"] = WRONG
            
            if st.session_state.choices.get(str(st.session_state.question_type)) is None:
                st.session_state.choices[str(st.session_state.question_type)] = [] # Initialize saving choices
            
            
            st.session_state.choices[str(st.session_state.question_type)].append((question, choice)) # Saves answer
            print(st.session_state[f"button_{question.id}{choice.id.lower()}_value"], "this is the value", correct_answer, "this is the correct answer")
            
            # print(f"Selected button: {selected_button}")  # Print the selected_button)
            
        
        
        for i, choice in enumerate(question.choices):
            # print(choice,"choice")
            st.session_state[f"button_{question.id}{choice.id.lower()}_value"] = st.session_state.get(f"button_{question.id}{choice.id.lower()}_value", 0) # Initialize state for each button
            # print(f"Initialized button_{question['id']}{choice[0].lower()}_value to {st.session_state[f'button_{question['id']}{choice[0].lower()}_value']}")
            value = st.session_state[f"button_{question.id}{choice.id.lower()}_value"] 
            st.button(
                f"{choice.id}. {choice.choice}", 
                on_click=on_choice_click, 
                key=f"button_{question.id}{choice.id.lower()}", 
                args=(choice, question), # TODO: fix the problem with correct answers being because it is only considering the last question
                disabled=value!=0, # Default value is 0, if the value changes (the user changed it, refer to on_choice_click) then it will disable.
                )

if st.session_state.question_type < len(exam.types):
    render_questions()
        


# --- NAVIGATION LOGIC ---

# Define the callback functions
def next_page():
    st.session_state.question_type += 1

def go_back():
    if st.session_state.question_type > 0:
        st.session_state.question_type -= 1

if st.session_state.question_type < len(exam.types):
    # Create a layout for buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.question_type > 0:
            st.button("Go back", on_click=go_back)

    with col2:
        # Check if we are on the very last category/page
        if st.session_state.question_type < len(exam.types) - 1:
            st.button("Next", on_click=next_page)
        else:
            # This only shows on the absolute last page
            if st.button("Complete Exam", on_click=next_page):
                st.balloons() # Optional flair!
                st.switch_page("pages/explanations.py") # Navigate to the explanations page after completing the exam

# --- SCORE DISPLAY ---
# This part handles the "Exam Completed" state
if st.session_state.question_type >= len(exam.types):
    st.switch_page("pages/explanations.py")
    
# INVISIBLE DATA

for key in st.session_state.keys(): # This adds a class that makes your answer right or wrong based on the previous iteration of the program.
    if key.startswith("button_"):
        key_part = key[:-6]
        if st.session_state[key] == 1:
            st.markdown(f"<style>.st-key-{key_part} {{ background-color: #30b31e; }}</style>", unsafe_allow_html=True)
        elif st.session_state[key] == 2:
            
            st.markdown(f"<style>.st-key-{key_part} {{ background-color: #872b2b; }}</style>", unsafe_allow_html=True)
        else:
            pass    
        
st.markdown(
    """
    <style>
    div.stButton {
        padding-left: 50px;
    }
    </style>
    """, unsafe_allow_html=True
)