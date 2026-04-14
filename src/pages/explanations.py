import json

import streamlit as st


def print_exam(exam:list):
    pass

st.title("Explanations")

st.write("# Completed Exam")


CHOICES = st.session_state.choices

score=0
correct_questions=[]
unanswered_questions=[]
wrong_questions=[]

EXAM=st.session_state.exam

total_questions = sum(len(page.questions) for page in EXAM.types)

CORRECT = 1
UNANSWERED = 0
WRONG = 2



score_type=st.toggle('Use "Right minus wrong"' )

for i, page in enumerate(EXAM.types):
    page=dict(page)
    unanswered_questions.extend(page)
    correct_questions.extend(page)
    wrong_questions.extend(page)
    
    for current_page in CHOICES[str(i)]:
        print("Current page",current_page)
        for question in current_page:
            print("unaswred questions", question)
            unanswered_questions[i].remove(question)
            if answer.id == question.correct_answer:
                wrong_questions[i].questions.remove(page[0])
                score+=1
            else:
                correct_questions[i].questions.remove(page[0])
                if score_type:
                    score-=0.25
        


st.write(f"Your final score is {score}/{total_questions}.")

question_type = st.radio("Select question type to review:", ("All","Correct", "Wrong", "Unanswered"))


