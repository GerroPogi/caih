import json
import streamlit as st

# class ExamList(list):
#     def __init__(self, *args):
#         super().__init__(*args)
#     def get_instructions(self,index=0):
#         return self[index][1]
#     def get_questions(self,index=0):
#         return self[index][0]
    
#     def remove_question(self,question, index=0):
#         print(f"{self[index][0][1]=}")
#         self[index][0][1].remove(question)

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
for i, page in enumerate(EXAM.types): # Page: (questions,[questions]),(instructions,"instruction")
    # page=dict(page)
    
    unanswered_questions.append(page)
    correct_questions.append(page)
    wrong_questions.append(page)
    # print("Un answered",unanswered_questions) 
    for question, answer in CHOICES[str(i)]:
        print("Un answers",question)
        unanswered_questions[i].questions.remove(question)
        if answer.id == question.correct_answer:
            wrong_questions[i].questions.remove(question)
            score+=1
        else:
            correct_questions[i].questions.remove(question)
            if score_type:
                score-=0.25
        


st.write(f"Your final score is {score}/{total_questions}.")

question_type = st.radio("Select question type to review:", ("All","Correct", "Wrong", "Unanswered"))


