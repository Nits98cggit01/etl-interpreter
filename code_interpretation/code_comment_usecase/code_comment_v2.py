import streamlit as st
import openai
import os

# Set the page to full screen
st.set_page_config(layout="wide")

# Set your OpenAI API key here
openai.api_key = "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"

st.title("Programming Language Interpreter")

# Action - Drop down to display the list of programming languages
programming_language = st.selectbox("Select Programming Language", ["Python", "SQL", "Java", "C++", "JavaScript"])

# Action - File uploader section to upload file
uploaded_file = st.file_uploader("Upload a .txt or .py file", type=["txt", "py"])

# Action - To create two sections using columns
left_column, right_column = st.columns(2)

# Function to detect programming language of the input/uploaded code snippet
def detect_programming_language(code):
    analyze_response = openai.Completion.create(
            engine="text-davinci-003",  # Use GPT-3.5 Turbo
            prompt=f'''Act as a compiler. Your task is to analyze the below code and find out what programming language the below code is. 
                    Make sure that you give only the programming language as the response. 
                    Response should be strictly one word!! :
                    \n{code}
                    ''',
            max_tokens=1024, 
            n=1,
            stop=None,
            temperature=0.3, 
        )
    detected_language = analyze_response.choices[0].text.strip()
    return detected_language

# Function to generate comments for the input/uploaded code snippet
def generate_comments(code):
    print("-------------------------------------------------------")
    print(f"The generate code is : {code}")
    response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=f'''Add comments to the {programming_language} code. 
                    Make sure that the entire code is displayed with the comment wherever necessary. 
                    The comments needs to be present on top of function definition, function call or the query block maintain good spacing and better readability :
                    \n{code}
                    ''',
            max_tokens=1024, 
            n=1,
            stop=None,
            temperature=0.7,
        )
    comments = response.choices[0].text.strip()
    return comments

def get_file_extension(file_name):
    return os.path.splitext(file_name)[1] if file_name else None


def format_comments_with_style(comments, style):
    lines = comments.split("\n")
    formatted_lines = []

    for line in lines:
        if line.strip().startswith("#"):  # You can adjust this condition for Python comments
            formatted_lines.append(f'<span style="{style}">{line}</span>')
        else:
            formatted_lines.append(line)

    return "\n".join(formatted_lines)

# Create a session state to keep track of the app's state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Use st.form to encapsulate the form elements
with st.form(key="programming_language_form"):
    # Action - Analyze button to check if the selected programming language matches with the detected language
    if uploaded_file is not None:
        input_code = uploaded_file.read().decode("utf-8")
        left_text_area = left_column.text_area("INPUT CODE", input_code, height=400)

        # Determine the file format (extension)
        file_extension = get_file_extension(uploaded_file.name)

        if st.form_submit_button("GENERATE"):
            detected_language = detect_programming_language(input_code)
            # st.write(f"Analyzer ran...The selected programming language {programming_language} is matching with the detected language {detected_language}. Click Submit to proceed with the interpreter")

            if detected_language == programming_language:
                st.write(f"Analyzer ran...The selected programming language {programming_language} is matching with the detected language {detected_language}. Please wait for few seconds...")
                st.session_state.submitted = True
            
            else:
                st.error(f"The selected programming language ({programming_language}) does not match the detected language ({detected_language}).")


# Check if the "Submit" button was clicked
if st.session_state.submitted:
    # Call a Python function to add comments using GPT-3.5 Turbo
    comments = generate_comments(left_text_area)
    right_text_area = right_column.text_area("Interpreter Output", value=comments, height=400)
    # right_column.markdown(f'<div style="color: blue;">{comments}</div>', unsafe_allow_html=True)

    # Format comments with a specific style (e.g., color: blue)
    #formatted_comments = format_comments_with_style(comments, 'color: blue;')

    # Display the formatted comments in the right text area
    #right_column.markdown(formatted_comments, unsafe_allow_html=True)

    # Add a download button to download the file in the same format
    with st.expander("Download Output"):
        st.write("Click the button below to download the output.")
        st.download_button(
            label="Download Output",
            data=comments,
            file_name=f"{uploaded_file.name}{file_extension}",
            key="download_button"
        )
