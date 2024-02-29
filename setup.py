from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='nikhil bansal',
    author_email='bansal562003@gmail.com',
    install_requires=["google-generativeai","google-ai-generativelanguage","langchain","streamlit","python-dotenv","PyPDF2","langchain-google-genai","cygrpc","grpcio"],
    packages=find_packages()
)