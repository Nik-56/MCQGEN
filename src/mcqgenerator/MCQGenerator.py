import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from grpc._cython import cygrpc
import streamlit as st
from grpc._typing import MetadataType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# GOOGLE_API_KEY = "AIzaSyBN7qOOuGRmhZf5lC8uu6hr1SOW6_7pFA4"
# st.secrets['GOOGLE_API_KEY']
# load_dotenv()
# os.getenv('GOOGLE_API_KEY')
header = {
"GOOGLE_API_KEY": st.secrets['GOOGLE_API_KEY']
}
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.7)



TEMPLATE="""
Text:{text}
You are an expert MCQ maker, given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be confirming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQ's
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt= PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2 = """"
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {Subject} students. You need to evaluate the complexity of the question and give a complete analysis of the quiz.
Only use at max 50 words for complexity if the quiz is not at per with the cognitive and analytical abilities of the students, update the quiz questions which needs to be changed and charge the
tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English writer of the above quiz and give a review of max 50 words:
{review}
"""

quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain= SequentialChain(chains=[quiz_chain, review_chain],
                                         input_variables=["text", "number", "subject", "tone", "response_json"],
                                         output_variables=["quiz", "review"], verbose=True,)

