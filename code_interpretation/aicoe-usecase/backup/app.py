import streamlit as st
import os
import openai


def askgpt(left_text):
    #Note: The openai-python library support for Azure OpenAI is in preview
    openai.api_type = "azure"
    openai.api_base = "https://llmdemo.openai.azure.com/"
    openai.api_version = "2022-12-01"
    openai.api_key = "7ae7bffcd56d4ee89f742dcf20b67269"

    response = openai.Completion.create(
    engine="gpt-35-turbo",
    prompt=f"write the below code with comments {left_text}",
    temperature=1,
    max_tokens=100,
    top_p=0.5,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)

    return response

# Set the page to full screen
st.set_page_config(layout="wide")

# Set the page title
st.title("AICOE - GEN AI CODE INTERPRETER")

# Dropdown list with 5 options
selected_option = st.selectbox("Select a programming language", ["PYTHON", "SQL", "JAVA", "C", "C++"])

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

# Create two sections using columns
left_column, right_column = st.columns(2)


# Text area on left and right
left_text = left_column.text_area("Input text area", "", height=400)
right_text = right_column.text_area("OUTPUT", "", height=400)

# Display the content of the uploaded text file in the left area
if uploaded_file is not None:
    left_text = uploaded_file.read()
    left_column.write("Uploaded Text File Content:")
    left_column.write(left_text)

# Submit button
if left_column.button("Submit"):
    right_column.write(f"You selected: {selected_option}")
    result = askgpt(left_text)
