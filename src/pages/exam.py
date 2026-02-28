import json

import streamlit as st

st.title("Exam Page")

@st.cache_data
def get_exam():
    exam = st.session_state.data.fetch_exam()
    sorted= {question["instruction"]:[] for question in exam} # Sorts by instruction of every item
    
    for question in exam:
        sorted[question["instruction"]].append(question)
    return sorted

# st.markdown("<style>button[kind='right'] { background-color: #30b31e; }</style>", unsafe_allow_html=True)
# st.markdown("<style>button[kind='wrong'] { background-color: #872b2b; }</style>", unsafe_allow_html=True)
# st.markdown("<style>button[kind='none'] { background-color: #8a877f; }</style>", unsafe_allow_html=True)
# button2_clicked = st.button("Button 2",type="primary")
# st.markdown(
#     """
#     <style>
#     .right {
#         background-color: #30b31e;
#     }
#     .wrong {
#         background-color: #872b2b;
#     }
#     .none {
#         background-color: #8a877f;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.markdown('<span id="right"></span>', unsafe_allow_html=True)
# st.button("My Button")



exam=get_exam()
# print(json.dumps(exam,indent=4))

exam_dict_key =list(exam.keys())[st.session_state.question_type] # Grabs the instructions
st.write(exam_dict_key)

def clean_choice(choice): # Brute force method to clean out choice in case when the AI adds extra text.
    while not choice[0].lower() in "abcd":
        choice=choice[1:]
    return choice

CORRECT = 1
WRONG = 2
DISABLED = 3

print(json.dumps(exam,indent=4))

for question in exam[exam_dict_key]:
    st.html(question["question"])
    def on_choice_click(choice,num):
        for disable_choice in question["choices"]:
            choice_name=f"button_{num}{disable_choice[0].lower()}_value"
            st.session_state[choice_name] = DISABLED
        choice = clean_choice(choice)
        selected_button_key=f"button_{num}{choice[0].lower()}_value"
        print(choice)
        if choice[0].lower() == "abcd"[question["correct_answer"]]:
            print("Correct!")
            st.session_state.score[num]=st.session_state.score.get(num,0)+1
            st.session_state[selected_button_key] = CORRECT
        else:
            print("Wrong.")
            st.session_state.score[num]=st.session_state.score.get(num,0)-1 # TODO - add a feedback system later on, or tell them if it's right or wrong
            st.session_state[selected_button_key] = WRONG

        # print(f"Selected button: {selected_button}")  # Print the selected_button)
        
    
    
    for choice in question["choices"]:
        choice=clean_choice(choice)
        st.session_state[f"button_{question['id']}{choice[0].lower()}_value"] = st.session_state.get(f"button_{question['id']}{choice[0].lower()}_value", 0) # Initialize state for each button
        # print(f"Initialized button_{question['id']}{choice[0].lower()}_value to {st.session_state[f'button_{question['id']}{choice[0].lower()}_value']}")
        value = st.session_state[f"button_{question['id']}{choice[0].lower()}_value"] 
        st.button(
            choice, 
            on_click=on_choice_click, 
            key=f"button_{question['id']}{choice[0].lower()}", 
            args=(choice,question["id"]),
            disabled=value!=0, # Default value is 0, if the value changes (the user changed it, refer to on_choice_click) then it will disable.
            # type="none" if value==0 else "right" if value==1 else "wrong"
            )
        


if st.button("Go back"):
    st.switch_page("main.py")

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