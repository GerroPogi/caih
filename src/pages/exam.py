import json,time

import streamlit as st

st.title("Exam Page")


@st.cache_resource
def get_exam(amount, subject, _data_fetcher):
    exam = _data_fetcher.fetch_exam(amount, subject)
    # Pre-process images HERE so it only happens once
    for category in exam.types:
        for q in category.questions:
            for img in q.images:
                q.question = q.question.replace(img.image_name, f"data:image/png;base64,{img.data}")
    
    st.session_state.timer.start(st.session_state.time_amount)
    return exam

def img_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

# Pass the dependencies as arguments
if st.session_state.exam is None:
    exam = get_exam(
        st.session_state.question_amount, 
        st.session_state.subject, 
        st.session_state.data
    )
else:
    exam = st.session_state.exam

timer = st.session_state.timer
if timer.ended:
    st.session_state.question_type = len(exam.types)
st.session_state.exam=exam
current_page_type = exam.types[min(st.session_state.question_type,len(exam.types)-1)]

if timer.started: # If there is an exam that has just been generated, it will show the timer, if there is no timer, it will not
    st.write(f"### Time left: {time.strftime('%M:%S', time.gmtime(timer.get_time_left()))}") 



CORRECT = 1
WRONG = 2
DISABLED = 3
def render_questions():
    exam_dict_key =current_page_type.instruction # Grabs the instructions
    st.write("## "+exam_dict_key)
    for question in current_page_type.questions:
        
        if len(question.images) != 0:
            for image in question.images:

                question.question = question.question.replace(image.image_name,f"data:image/png;base64,{image.data}")
            st.markdown(f"#### {question.id}.  {question.question}", unsafe_allow_html=True) 
        else:
            st.markdown(f"#### {question.id}.  {question.question}", unsafe_allow_html=True)
        def on_choice_click(button_id,choice, selected_question):
            correct_answer = selected_question.correct_answer
            question_state= st.session_state.question_states[selected_question.id]
            
            for button in question_state.keys():
                question_state[button] = DISABLED
            if choice.id == correct_answer:
                question_state[button_id] = CORRECT
            else:
                question_state[button_id]= WRONG
            if st.session_state.choices.get(str(st.session_state.question_type)) is None:
                st.session_state.choices[str(st.session_state.question_type)] = [] # Initialize saving choices
            
            
            st.session_state.choices[str(st.session_state.question_type)].append((selected_question, choice)) # Saves answer
        
        st.session_state.question_states[question.id] = st.session_state.question_states.get(question.id, {})
        question_state=st.session_state.question_states[question.id]
        for i, choice in enumerate(question.choices):
            # st.session_state[f"button_{question.id}{choice.id.lower()}_value"] = st.session_state.get(f"button_{question.id}{choice.id.lower()}_value", 0) 
            
            # print(f"Initialized button_{question['id']}{choice[0].lower()}_value to {st.session_state[f'button_{question['id']}{choice[0].lower()}_value']}")
            # value = st.session_state[f"button_{question.id}{choice.id.lower()}_value"] 
            button_id=f"button_{question.id}{choice.id.lower()}"
            # if st.session_state.get(choice.id) is not None:
            #     for i in range(1, len(st.session_state.keys())): # When AI adds too much choices
            #         if st.session_state.get(button_id+str(i)) is None:
            #             button_id=button_id+str(i)
            #             break
            question_state[button_id] = question_state.get(button_id, 0) # Initialize state for each button
            
            # print(button_id)
            st.button(
                f"{choice.choice}", 
                on_click=on_choice_click, 
                key=button_id, 
                args=(button_id,choice, question), # TODO: fix the problem with correct answers being because it is only considering the last question
                disabled=question_state[button_id]!=0, # Default value is 0, if the value changes (the user changed it, refer to on_choice_click) then it will disable.
                use_container_width=False
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

for key, choices in st.session_state.question_states.items(): # This adds a class that makes your answer right or wrong based on the previous iteration of the program.
    for button_id, choice in choices.items():
        if choice == CORRECT:
            st.markdown(f"<style>.st-key-{button_id} {{ background-color: #30b31e; }}</style>", unsafe_allow_html=True)
        elif choice == WRONG:
            
            st.markdown(f"<style>.st-key-{button_id} {{ background-color: #872b2b; }}</style>", unsafe_allow_html=True)
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

# Instead of just st.rerun()
if not timer.ended:
    time.sleep(0.1) # Prevents the script from pegged CPU usage
    st.rerun()