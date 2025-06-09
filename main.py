# this is a Streamlit app that allows users to upload their resumes in PDF format and get feedback on how to improve them using OpenAI's API.
# streamlit is a Python library that makes it easy to create web applications for data science and machine learning projects.
# the goal of this app is to help users improve their resumes by providing feedback based on the job role they are applying for.
import streamlit as st
import PyPDF2
import io 
import os
from openai import OpenAI  
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Set up the Streamlit app configuration
# Set the page title, icon, and layout

st.set_page_config(page_title="AI resume critiquer", page_icon=":page:", layout="centered")
st.title("AI Resume Critiquer")
st.markdown("Upload your resume in PDF format and get feedback on how to improve it.")

# Initialize OpenAI client 
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# this is the main part of the app where users can upload their resumes and specify the job role they are applying for.
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
job_role = st.text_input("Enter the job role you are applying for")
# this is the button that users can click to analyze their resumes and get feedback.
analyze_button = st.button("Analyze Resume")
# This function reads the PDF file and extracts text from each page.
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    # Loop through each page in the PDF and extract text
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
    # Extract text from uploaded file based on its type
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read())) 
    return uploaded_file.read().decode("utf-8")
# Check if the analyze button is clicked and a file is uploaded
if analyze_button and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read.")
            st.stop()
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
        st.stop()
 # Generate feedback using OpenAI's API       
# The OpenAI client is already initialized as 'openai_client' above, so you can use 'openai_client' directly.

    # Construct the prompt using the extracted resume text and job role
    prompt = f"Job Role: {job_role}\nResume:\n{file_content}\n\nPlease provide detailed feedback on how to improve this resume for the specified job role."

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert resume reviewer with extensive experience in evaluating resumes for various job roles. Your task is to provide constructive feedback on how to improve the resume based on the job role provided."},
            {"role": "user", "content": prompt}
        ],
        # Set the maximum number of tokens for the response
        max_tokens=500,
        temperature=0.5
    )
    # Display the result in the Streamlit app
    st.markdown("### Result:")
    st.markdown(response.choices[0].message.content)

    
    