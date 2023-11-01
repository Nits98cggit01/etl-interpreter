import streamlit as st
import openai

# Set the page to full screen
st.set_page_config(layout="wide")

# Set your OpenAI API key here
openai.api_key = "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"

# Streamlit UI components
st.title("Gen AI - Programming language interpreter")

# Dropdown for selecting programming language
programming_language = st.selectbox("Select Programming Language", ["Python", "SQL" ,"Java", "C++", "JavaScript"])

# File uploader for code
uploaded_file = st.file_uploader("Upload a .txt or .py file", type=["txt", "py"])

# Create two sections using columns
left_column, right_column = st.columns(2)

# # Text areas for displaying code and comments
# left_text_area = left_column.text_area("INPUT CODE", "", height=400)
# right_text_area = right_column.text_area("OUTPUT", "", height=400)

# Submit button
# if st.button("Submit"):
if uploaded_file:
    # Read the uploaded file
    code_content = uploaded_file.read().decode("utf-8")
    left_text_area = left_column.text_area("INPUT CODE", code_content, height=400)

    if st.button("Analyze"):
        analyze_response = openai.Completion.create(
            engine="text-davinci-003",  # Use GPT-3.5 Turbo
            prompt=f'''Act as a compiler. Your task is to analyze the below code and find out what programming language the below code is. 
                    Make sure that you give only the programming language as the response. 
                    Response should be strictly one word!! :
                    \n{code_content}
                    ''',
            max_tokens=1024,  # Adjust as needed
            n=1,
            stop=None,
            temperature=0.3,  # Adjust for creativity
        )
            
        # Display the generated comments
        check_language = analyze_response.choices[0].text
        st.write(f"Check language : {check_language}")
        st.write(f"Programming lan : {programming_language}")
        print(check_language)
        print(programming_language)

        if check_language != programming_language:
        #     print("Failed")
        #     st.error(f"The chosen programming language is {programming_language} and uploaded file contains {check_language} code snippet... Please re-upload correct file")

        # else:
            print("Success")
            if st.button("Submit"):
            # Call GPT-3.5 Turbo model to generate comments
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Use GPT-3.5 Turbo
                    prompt=f'''Add comments to the {programming_language} code. 
                            Make sure that the entire code is displayed with the comment wherever necessary. 
                            The comments should be crisp and present in the beggining of the code block to maintain good spacing and better readability :
                            \n{code_content}
                            ''',
                    max_tokens=1024,  # Adjust as needed
                    n=1,
                    stop=None,
                    temperature=0.5,  # Adjust for creativity
                )
                    
                # Display the generated comments
                comments = response.choices[0].text
                print(comments)
                right_text_area = right_column.text_area("OUTPUT", comments, height=400)
