import streamlit as st
from PyPDF2 import PdfReader
from together import Together
import base64
import io
import re
import os
from dotenv import load_dotenv
load_dotenv()

st.markdown(
    """
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    # padding-left: 2rem;
                    # padding-right:2rem;
                }
        </style>
        """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_models():
    api_key = os.environ['TOGETHER_API_KEY']  

    # Initialize Together client
    client = Together(api_key=api_key)
    return client


def extract_references(text):
    # Define a regex pattern to match the References section and its content
    pattern = r'References\s+(\[.*?\])'
    
    # Search for the pattern in the provided text
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        # Extract the matched references section
        references = match.group(1)
        return references
    else:
        return "References section not found."


def research_paper():

    col1, col2 = st.columns([2,1],gap='large')
    uploaded_file = None
    with col1:

        st.title("Research Paper Submission")
        uploaded_file = st.file_uploader("Choose a file", type=['pdf'])
    
    if uploaded_file is not None:
        
        pdf_data = uploaded_file.read()
        # Convert bytes to a file-like object
        pdf_stream = io.BytesIO(pdf_data)
        reader = PdfReader(pdf_stream)
        
        with col2:
            b64_pdf = base64.b64encode(pdf_data).decode("utf-8")
            pdf_display = f'<embed src="data:application/pdf;base64,{b64_pdf}" width="520" height="750" type="application/pdf">'
            st.write("")
            st.markdown(pdf_display, unsafe_allow_html=True)
            num_references = st.slider("Enter the number of pages which have references", min_value=1, max_value=len(reader.pages), value=0)
            
        with col1:
            # Store the pdf text for the last num_references pages only
            last_pages_text = ''
            for page in reader.pages[-num_references:]:
                last_pages_text += page.extract_text()
            st.write("Text of last {} pages:".format(num_references))
            st.write(last_pages_text)
            
    else:
        st.warning("Please upload a file.")


llm = load_models()
research_paper()