import streamlit as st
import openai

# Set the page to full screen
st.set_page_config(layout="wide")


openai.api_key = "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"

def highlight_human_generated_content(input_paragraph):
    # Define the criteria for human-generated content
    criteria = [
        "Grammatical error",
        "Out of the context",
        "Spelling error",
        "Unwanted use of abbreviations",
        "Inconsistent use of Punctuation marks",
        "Inconsistency of content flow"
    ]

    # Generate AI response using GPT-3.5 model
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f'''Act as a python developer with a strong generative AI background. Your task is to distinguish the human generated content and ai generated content from the input text. The human generated content can be identified if the input paragraph contains any of the following {criteria}. The input paragraph is : {input_paragraph}''',
        max_tokens=1024,  
        stop=None,
        temperature=0.2, 
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the AI-generated content from the response
    prompt=f'''Act as a python developer with a strong generative AI background. Your task is to distinguish the human generated content and ai generated content from the input text. The human generated content can be identified if the input paragraph contains any of the following {criteria}. The input paragraph is : {input_paragraph}'''
    ai_generated_content = response.choices[0].text.strip()
    st.write(prompt)
    # Compare the input paragraph and AI-generated content to identify human-generated content
    highlighted_content = ""
    for sentence in input_paragraph.split('. '):
        if sentence not in ai_generated_content:
            # Check if the sentence contains any of the specified criteria
            if any(criteria_word.lower() in sentence.lower() for criteria_word in criteria):
                highlighted_content += f"\033[91m{sentence.strip()}. \033[0m"  # Highlight in red
            else:
                highlighted_content += f"{sentence.strip()}. "
        else:
            highlighted_content += f"{sentence.strip()}. "

    # Print the highlighted content
    return highlighted_content



# Streamlit app
st.title("AI Content Identifier")

# File uploader section
st.header("Upload a Text File")
uploaded_file = st.file_uploader("Choose a file", type=["txt"])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    st.text_area('File Content', content, height=300)
    # st.write(content)

    # Detect button
    if st.button("Detect"):
        highlighted_text = highlight_human_generated_content(content)
        st.text_area('Output Content', highlighted_text, height=300)
        # st.subheader("Highlighted Content:")
        # st.write(highlighted_text)