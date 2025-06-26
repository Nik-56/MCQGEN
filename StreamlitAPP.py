import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

header = {
    "GOOGLE_API_KEY": st.secrets['GOOGLE_API_KEY']
}

with open(r'Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQ Generator")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or text file")

    mcq_count = st.number_input("Number of MCQ's", min_value=3, max_value=50)

    subject = st.text_input("Insert Subject", max_chars=25)

    tone = st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Create MCQ's")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)

                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        # Clean the quiz string before processing
                        quiz = quiz.replace('### RESPONSE_JSON\n', '')
                        
                        # Debug: Show what we're trying to parse
                        st.write("Debug - Quiz content:", quiz[:200] + "..." if len(quiz) > 200 else quiz)
                        
                        table_data = get_table_data(quiz)
                        if table_data is not None and len(table_data) > 0:  # Fixed condition
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            
                            # Also show review if available
                            review = response.get("review", None)
                            if review:
                                st.subheader("Review")
                                st.write(review)
                        else:
                            st.error("Error in the table data - could not parse quiz format")
                            st.write("Raw quiz data:", quiz)  # Show raw data for debugging
                    else:
                        st.error("No quiz found in response")
                        st.write("Full response:", response)
                
                else:
                    st.write("Unexpected response format:")
                    st.write(response)