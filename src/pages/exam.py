import json

import streamlit as st

st.title("Exam Page")

@st.cache_data
def get_exam():
    print(st.session_state.data.fetch_exam)
    exam = st.session_state.data.fetch_exam(st.session_state.question_amount,st.session_state.subject)
    return exam


exam=get_exam()
st.session_state.exam=exam
print(json.dumps(exam,indent=4)) # Only use for debugging 
# print(st.session_state.question_type,len(exam))

current_page_type = exam[min(st.session_state.question_type,len(exam)-1)]


def clean_choice(choice): # Brute force method to clean out choice in case when the AI adds extra text.
    while not choice[0].lower() in "abcd":
        choice=choice[1:]
    return choice

CORRECT = 1
WRONG = 2
DISABLED = 3
def render_questions():
    exam_dict_key =exam[st.session_state.question_type]["instruction"] # Grabs the instructions
    st.write(exam_dict_key)
    for question in exam[st.session_state.question_type]["questions"]:
        st.markdown(f"{question['id']}.  {question['question']}", unsafe_allow_html=True)
        def on_choice_click(button_choice,num:int ):
            print(button_choice,num)
            for disable_choice in "abcd":
                choice_name=f"button_{num}{disable_choice[0].lower()}_value"
                st.session_state[choice_name] = DISABLED
            button_choice = clean_choice(button_choice)
            selected_button_key=f"button_{num}{button_choice[0].lower()}_value"
            print(button_choice)
            st.session_state.choices[num]=button_choice[0].lower() # Store the user's choice for later reference in explanations page            
            correct_answer=0
            for question in current_page_type["questions"]:
                if question["id"]==num:
                    correct_answer=question["correct_answer"] 
            
            if button_choice[0].lower() == "abcd"[correct_answer]:
                print("Correct!")
                st.session_state.score[str(num)]=CORRECT
                st.session_state[selected_button_key] = CORRECT
            else:
                print("Wrong.")
                st.session_state.score[str(num)]=WRONG
                st.session_state[selected_button_key] = WRONG
            print("correct answer: ","abcd"[current_page_type["questions"][int(num)-1]["correct_answer"]],num)

            # print(f"Selected button: {selected_button}")  # Print the selected_button)
            
        
        
        for i, choice in enumerate(question["choices"]):
            choice=clean_choice(choice)
            st.session_state[f"button_{question['id']}{choice[0].lower()}_value"] = st.session_state.get(f"button_{question['id']}{choice[0].lower()}_value", 0) # Initialize state for each button
            # print(f"Initialized button_{question['id']}{choice[0].lower()}_value to {st.session_state[f'button_{question['id']}{choice[0].lower()}_value']}")
            value = st.session_state[f"button_{question['id']}{choice[0].lower()}_value"] 
            st.button(
                choice, 
                on_click=on_choice_click, 
                key=f"button_{question['id']}{"abcd"[i]}", 
                args=(choice,question["id"]), # TODO: fix the problem with correct answers being because it is only considering the last question
                disabled=value!=0, # Default value is 0, if the value changes (the user changed it, refer to on_choice_click) then it will disable.
                )

if st.session_state.question_type < len(exam):
    render_questions()
        


# --- NAVIGATION LOGIC ---

# Define the callback functions
def next_page():
    st.session_state.question_type += 1

def go_back():
    if st.session_state.question_type > 0:
        st.session_state.question_type -= 1

if st.session_state.question_type < len(exam):
    # Create a layout for buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.question_type > 0:
            st.button("Go back", on_click=go_back)

    with col2:
        # Check if we are on the very last category/page
        if st.session_state.question_type < len(exam) - 1:
            st.button("Next", on_click=next_page)
        else:
            # This only shows on the absolute last page
            if st.button("Complete Exam", on_click=next_page):
                st.balloons() # Optional flair!
                st.switch_page("pages/explanations.py") # Navigate to the explanations page after completing the exam

# --- SCORE DISPLAY ---
# This part handles the "Exam Completed" state
if st.session_state.question_type >= len(exam):
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