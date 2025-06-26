import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            # Fix for newer PyPDF2 versions
            pdf_reader = PyPDF2.PdfReader(file)  # Changed from PdfFileReader
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            print(f"Error reading PDF: {e}")
            raise Exception("Error reading the PDF File")
    
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "Unsupported file format only pdf and text file supported."
        )
    
def get_table_data(quiz_str):
    try:
        # Clean the quiz string - remove any markdown formatting
        quiz_str = quiz_str.strip()
        if quiz_str.startswith('```json'):
            quiz_str = quiz_str[7:]  # Remove ```json
        if quiz_str.endswith('```'):
            quiz_str = quiz_str[:-3]  # Remove ```
        quiz_str = quiz_str.strip()
        
        # Remove any additional formatting
        quiz_str = quiz_str.replace('### RESPONSE_JSON\n', '')
        
        print(f"Attempting to parse JSON: {quiz_str[:200]}...")  # Debug print
        
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                ]
            )

            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except Exception as e:
        print(f"Error in get_table_data: {e}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return None  # Return None instead of False for consistency