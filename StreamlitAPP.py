import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain


with open(r'C:\Users\Nikhil\OneDrive\Documents\Desktop\openai\MCQGEN\Response.json', 'r') as file:
    RESPONSE_JSON=json.load(file)

st.title("MCQ Generator")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or text file")

    mcq_count= st.number_input("Number of MCQ's", min_value=3, max_value=50)

    subject= st.text_input("Insert Subject", max_chars=25)

    tone= st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    button= st.form_submit_button("Create MCQ's")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text=read_file(uploaded_file)

                response=generate_evaluate_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    quiz=response.get("quiz", None)
                    quiz = quiz.replace('### RESPONSE_JSON\n', '')
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                        else:
                            st.error("Error in the table data")
                
                else:
                    st.write(response)
