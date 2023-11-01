import streamlit as st
import openai
import re
import os
import token
import nltk
nltk.download('punkt')

def chunk_large_code(code_chunk):
    """Split a large code chunk into meaningful chunks without breaking any loops or conditional statements.

    Args:
      code_chunk (str): The code chunk to split.

    Returns:
      list of str: List of smaller code chunks.
    """
    if not code_chunk:
        return []

    chunk = ''
    chunks = []

    # Iterate over the lines of code.
    for line in code_chunk.splitlines():
        # If the line contains the beginning of a loop or conditional statement,
        # create a new chunk for the loop or conditional statement.
        if re.match(r'\s*(for|while|if|elif|else|try|except|class|async def)\s+', line):
            if chunk:
                chunks.append(chunk)
            chunk = line
        else:
            # Add the line to the current chunk.
            chunk += '\n' + line

    # Add the last chunk.
    if chunk:
        chunks.append(chunk)

    return chunks

def estimate_tokens(text):
    words = nltk.word_tokenize(text)
    return len(words)

def get_code_chunks(code_content, programming_language):
    """Split code content into meaningful chunks based on language-specific patterns.

    Args:
        code_content (str): The code content.
        programming_language (str): The programming language of the code content.

    Returns:
        list of str: List of code chunks.
    """
    # Define regular expressions for different programming languages.
    language_patterns = {
        "Python": r'(?:(?<=\n\n)|(?<=\n))(?:def|for|while|if|elif|else|try|except|class|async def)\s+',
        "Java": r'(?:(?<=\n\n)|(?<=\n))(?:public|private|protected|static)?\s*\w+\s+\w+\s*\([^)]*\)\s*\{',
        "C++": r'(?:(?<=\n\n)|(?<=\n))\w+\s*\([^)]*\)\s*\{',
        "JavaScript": r'(?:(?<=\n\n)|(?<=\n))function\s+\w+\s*\([^)]*\)\s*\{',
        "SQL": r'(?:(?<=\n\n)|(?<=\n))CREATE FUNCTION\s+\w+\s*\([^)]*\)\s*RETURNS',
        "PySpark": r'(?:(?<=\n\n)|(?<=\n))\s*(?:def|val|var)\s+\w+\s*\([^)]*\)\s*:',
    }

    # Get the pattern based on the programming language.
    pattern = language_patterns.get(programming_language)
    if not pattern:
        raise ValueError("Unsupported programming language")

    # Split the code into chunks based on language-specific patterns.
    chunks = re.split(pattern, code_content)

    # Ensure that the first keyword of each chunk is included in the chunk.
    for i in range(len(chunks)):
        if not re.match(r'\s*\w+\s+', chunks[i]):
            # Get the keyword from the language pattern.
            keywords = re.findall(pattern, code_content)
            if keywords:
                keyword = keywords[i - 1] if i > 0 else keywords[i]
                chunks[i] = keyword + chunks[i]

    return chunks

# Set the page to full screen
st.set_page_config(layout="wide")

# Set your OpenAI API key here
openai.api_key = "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"

# Streamlit UI components
st.title("Gen AI - Programming language interpreter")

# Dropdown for selecting programming language
programming_language = st.selectbox("Select Programming Language", ["Python", "SQL", "Java", "C++", "JavaScript", "PySpark"])

# File uploader for code
uploaded_file = st.file_uploader("Upload a .txt or .py file", type=["txt", "py"])

# Create two sections using columns
left_column, right_column = st.columns(2)

# Create a folder to store code chunks
if not os.path.exists("code_chunks"):
    os.makedirs("code_chunks")

# Submit button
if uploaded_file:
    # Read the uploaded file
    code_content = uploaded_file.read().decode("utf-8")
    left_text_area = left_column.text_area("INPUT CODE", code_content, height=400)

    # Check if the code has fewer than 20 lines, if so, don't chunk.
    if code_content.count('\n') < 20:
        chunks = [code_content]
    else:
        # Split the code into meaningful chunks.
        chunks = get_code_chunks(code_content, programming_language)
        token_limit = 1500 # Token limit for chunking

    # Generate comments for each chunk and store in files
    comments = []
    output_chunks = []

    st.write("Chunks count")
    st.write(len(chunks))
    for i, chunk in enumerate(chunks):
        chunk_tokens = estimate_tokens(chunk)
        st.write("chunk_tokens")
        st.write("##################################", chunk_tokens, "#########################################")


        st.write("Chunk")
        st.write("##################################", chunk, "##########################################")
        if chunk_tokens is not None:
            # Check if the chunk exceeds the token limit
            if chunk_tokens >= token_limit:
                large_chunks = chunk_large_code(chunk)
                st.write("large_chunks")
                st.write("##############################################", large_chunks, "##########################")
                for j, large_chunk in enumerate(large_chunks):
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=f'''Act as a python compiler. Your task is to add comments to the uploaded code chunks.
                            Make sure that the entire code is displayed with the comments wherever necessary.
                            If there is a import statement, add "importing python package" as comment and nothing else!!
                            The comments need to be in a separate line to maintain good spacing and better readability:
                            \n{large_chunk}
                                ''',
                        max_tokens=token_limit,
                        n=1,
                        stop=None,
                        temperature=0.1,
                    )
                    # Save the chunk to a separate text file
                    chunk_filename = f"code_chunks/{os.path.splitext(uploaded_file.name)[0]}_chunk_{i + 1}_{j + 1}.txt"
                    with open(chunk_filename, "w") as chunk_file:
                        chunk_file.write(large_chunk)

                    # Display the generated comments
                    comments = response.choices[0].text
                    st.write("############################################### Comments_2 ########################")
                    st.write(comments)
                    output_chunks.append(comments)
            else:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f'''Act as a python compiler. Your task is to add comments to the uploaded code chunks.
                            Make sure that the entire code is displayed with the comments wherever necessary.
                            If there is a import statement, add "importing python package" as comment and nothing else!!
                            The comments need to be in a separate line to maintain good spacing and better readability:
                            \n{chunk}
                            ''',
                    max_tokens=token_limit,
                    n=1,
                    stop=None,
                    temperature=0.1,
                )
                # Save the chunk to a separate text file
                chunk_filename = f"code_chunks/{os.path.splitext(uploaded_file.name)[0]}_chunk_{i + 1}.txt"
                with open(chunk_filename, "w") as chunk_file:
                    chunk_file.write(chunk)

                # Display the generated comments
                comments = response.choices[0].text
                st.write("############################################### Comments ########################")
                st.write(comments)
                output_chunks.append(comments)

    # Merge the output chunks back into the original structure
    merged_code = "\n".join(output_chunks)
    output_filename = f"code_chunks/{os.path.splitext(uploaded_file.name)[0]}_Output.txt"
    with open(output_filename, "w") as output_file:
        output_file.write(merged_code)

    # Display the chunked code and comments
    right_text_area = right_column.text_area("OUTPUT", merged_code, height=400)



### Notes : Chunking is happening correctly. Chunks are being saved. 
# Def key word is not missing and others are missing.
# Not stable version.
# Token count is being considered.
# Large chunk issue has been handled and integrated with the model. Issue -> The output is random
