import json, copy
import streamlit as st
from datafetch.exam_model import QuestionList
from typing import List

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

def lower_headings(markdown: str, amount: int = 1):
    line_by_line = markdown.split("\n")
    new_lines = []
    
    for line in line_by_line:
        if line.startswith("#"):
            # Add the extra hashes to the start
            new_lines.append("#" * amount + line)
        else:
            new_lines.append(line)
            
    return "\n".join(new_lines)

@st.cache_resource
def create_lesson(exam:List[QuestionList]):
    st.session_state.lesson = st.session_state.data.create_lesson(exam)
    st.switch_page("pages/lesson.py")
    

def print_exam(exam:List[QuestionList], is_all=False):
    for question_list in exam:
        if len(question_list.questions) ==0:
            continue
        st.markdown(f"# {question_list.instruction}")
        
        for question in question_list.questions:
            st.markdown(f"## {question.id}.  {question.question}", unsafe_allow_html=True)
            if question.answer == None:
                st.write("You did not answer this question")
                print(question.answer)
                pass
            else:
                user_answer = question.get_choice(question.answer)
                st.write(f"Your answer: {user_answer.choice}")
            
            st.write(f"Correct answer: {question.get_choice(question.correct_answer).choice}")
            st.write("---"+"\n\n"
                        +lower_headings(question.explanation,1)+"\n\n" 
                        + "---", unsafe_allow_html=True)
    if st.button("Create a new lesson"):
        create_lesson(exam)

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
    
    unanswered_questions.append(copy.deepcopy(page))
    correct_questions.append(copy.deepcopy(page))
    wrong_questions.append(copy.deepcopy(page))
    # print("Un answered",unanswered_questions) 
    for question, answer in CHOICES[str(i)]:
        try:
            unanswered_questions[i].delete_question(question.id)
        except:
            pass
        if answer.id == question.correct_answer: # Correct
            wrong_questions[i].delete_question(question.id)
            correct_questions[i].add_answer(question.id, answer.id)
            page.add_answer(question.id, answer.id)
            score+=1
        else: # Wrong
            correct_questions[i].delete_question(question.id)
            wrong_questions[i].add_answer(question.id, answer.id)
            page.add_answer(question.id, answer.id)
            if score_type:
                score-=0.25
        


st.write(f"Your final score is {max(score,0)}/{total_questions}.")

question_type = st.radio("Select question type to review:", ("All","Correct", "Wrong", "Unanswered"))

if question_type == "Correct":
    print_exam(correct_questions)
elif question_type == "Wrong":
    print_exam(wrong_questions)
elif question_type == "Unanswered":
    print_exam(unanswered_questions)
else:
    print_exam(EXAM.types)

if st.button("Go Home"):
    st.switch_page("main.py")