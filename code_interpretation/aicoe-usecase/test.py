import streamlit as st
import openai

# Set the page to full screen
st.set_page_config(layout="wide")

# Set your OpenAI API key here
openai.api_key = "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"


st.title("Gen AI - Programming language interpreter")

# Action - Drop down to display the list of programming languages
programming_language = st.selectbox("Select Programming Language", ["Python", "SQL" ,"Java", "C++", "JavaScript"])

# Action - File uploader section to upload file
uploaded_file = st.file_uploader("Upload a .txt or .py file", type=["txt", "py"])

# Action - To create two sections using columns
left_column, right_column = st.columns(2)

# Function to detect programming language of the input/uploaded code snippet
def detect_programming_language(code):
    print(code)
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
    response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=f'''Add comments to the {programming_language} code. 
                    Make sure that the entire code is displayed with the comment wherever necessary. 
                    The comments needs to be in the separate line maintain good spacing and better readability :
                    \n{code}
                    ''',
            max_tokens=1024, 
            n=1,
            stop=None,
            temperature=0.7,
        )
    comments = response.choices[0].text.strip()
    return comments


# Action - Analyze button to check if the selected programming language matches with the detected language
if uploaded_file is not None:
    input_code = uploaded_file.read().decode("utf-8")
    left_text_area = left_column.text_area("INPUT CODE", input_code, height=400)

    analyzer_place = st.empty()
    if analyzer_place.button("Analyze"):
        detected_language = detect_programming_language(input_code)
        analyzer_place.empty()
        st.write(f"Analyzer ran...The selected programming language {programming_language} is matching with the detected language {detected_language}. Click Submit to proceed with interpreter")
        
        if detected_language == programming_language:
            print("Code entered this block")
            with left_column:
                if st.button("Submit"):
                    print("Submit triggered...")
                    # 8. Call a Python function to add comments using GPT-3.5 Turbo
                    print(f"Submit : {left_text_area}")
                    comments = generate_comments(left_text_area)
                    print(comments)
                    right_text_area = right_column.text_area("Interpreter Output", value=comments, height=400)
        else:
            st.error(f"The selected programming language ({programming_language}) does not match the detected language ({detected_language}).")




# if st.button("Analyze"):
#     if uploaded_file is not None:
#         # 6. Call a Python function to send an API call to GPT-3.5 Turbo to determine the programming language
#         input_code = uploaded_file.read().decode("utf-8")
#         detected_language = detect_programming_language(input_code)
#         left_text_area = left_column.text_area("INPUT CODE", input_code, height=400)

#         # 7. Check if the detected_language matches the selected_language
#         if detected_language == programming_language:
#             print("Code entered this block")
#             if st.button("Submit"):
#                 print("Submit triggered...")
#                 # 8. Call a Python function to add comments using GPT-3.5 Turbo
#                 print(f"Submit : {input_code}")
#                 comments = generate_comments(input_code)
#                 print(comments)
#                 right_text_area = right_column.text_area("Interpreter Output", value=comments, height=400)
#         else:
#             st.error(f"The selected programming language ({programming_language}) does not match the detected language ({detected_language}).")
