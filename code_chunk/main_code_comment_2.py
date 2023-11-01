import streamlit as st
import openai
import zipfile
import code2flow
import re
import os
import token
import nltk
from PIL import Image
nltk.download('punkt')

#============================ Code graph and code comment functions ============================
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
    #print("-------------------------------------------------------")
    #print(f"The generate code is : {code}")
    response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=f'''Add comments to the {programming_language} code. 
                    Make sure that the entire code is displayed with the comment wherever necessary. 
                    The comments needs to be present on top of function definition, function call or the query block maintain good spacing and better readability :
                    \n{code}
                    ''',
            max_tokens=2000, 
            n=1,
            stop=None,
            temperature=0.7,
        )
    comments = response.choices[0].text.strip()
    print(response)
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

# creates a folder in the base folder
def create_folder_in_base(new_folder_name):
    folder_path = os.path.join(base_folder, new_folder_name)
    # if new_folder_name != "":
    try:
        os.makedirs(folder_path)#, exist_ok=True)
        st.success(f"Created a new folder named '{new_folder_name}' in '{base_folder}'")
    except Exception as e:
        st.error(f"An error occurred: {e}")
   
    # elif new_folder_name == "":
    #     st.error("Please provide a name for the folder.")
        
    return folder_path

def process_zip_files(zip_file):
    # Extract the zip file name without the extension
    zip_file_name = os.path.splitext(zip_file.name)[0]

    # Create a folder with the same name as the zip file in the base folder
    extraction_folder = create_folder_in_base(zip_file_name)

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(extraction_folder)

    # List the contents of the extraction folder
    st.header(f"Contents of '{zip_file.name}' after extraction:")
    extraction_contents = os.listdir(extraction_folder)
    for item in extraction_contents:
        st.write(item)

def upload_selected_files(selected_files_list, selected_folder):
    # Get the folder path for saving
    folder_path = os.path.join(base_folder, selected_folder)
    if selected_folder != "Select a folder":
        if st.button("Upload files"):
            # Iterate through uploaded files and save them to the selected folder
            for selected_file in selected_files_list:
                with open(os.path.join(folder_path, selected_file.name), "wb") as f:
                    f.write(selected_file.read())
            st.success(f"Files Uploaded to {folder_path}")
            
def get_files_from_folder(selected_folder):
    # List files in the selected folder
    folder_path = os.path.join(base_folder, selected_folder)
    folder_contents = os.listdir(folder_path)

    # Filter only files (excluding subdirectories)
    #files_in_folder = [item for item in folder_contents if os.path.isfile(os.path.join(folder_path, item))]
    files_in_folder = [item for item in folder_contents if os.path.isfile(os.path.join(folder_path, item))]
    
    return files_in_folder

# Function to get the selected file based on user input
def get_selected_file(files_in_folder):
    # Extract file names from uploaded_files
    file_names = [file for file in files_in_folder]

    # Create a dropdown to select a file by name
    selected_file_name = st.selectbox(label="Select a file to display:", options=["None"] + file_names)

    # Return the selected file
    selected_file = None
    if selected_file_name:
        for file in files_in_folder:
            if file == selected_file_name:
                selected_file = file
    return selected_file

def get_folder_list(base_folder):
    try:
        folder_list = [folder for folder in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, folder))]
        return folder_list
    except Exception as e:
        if str(e) == "[WinError 3] The system cannot find the path specified: 'code_folders'":
            return st.error("Please create a folder from above before moving ahead.")
        else:
            return st.error(f'Error: "{str(e)}"')

# Function to generate graph for the code flow
def generate_graph(item_selected, input_dir):
    
    if isinstance(item_selected, list) and len(item_selected) > 0: # for converting whole project folder
        source_files = [os.path.join(input_dir, file) for file in item_selected if "." in file and file.split(".")[1] == "py"]
        output_file_path = ""
        
        if not os.path.exists(os.path.join(input_dir, "graph_output")):
            new_graph_output_folder = os.mkdir(os.path.join(input_dir, "graph_output"))
            output_file_path = os.path.join(input_dir, "graph_output", "graph.png")
        else:
            output_file_path = os.path.join(input_dir, "graph_output", "graph.png")
        
        graph_gen_instance = code2flow.code2flow(source_files, output_file=output_file_path, hide_legend=False, no_trimming=True)
        success_output_banner = st.success("Graph output has been successfully downloaded in {}".format(output_file_path))
        final_output_dict = {"graph_op": success_output_banner, "flag": 1, "output_image_path": output_file_path}
        return final_output_dict
    
    elif isinstance(item_selected, str) and item_selected != "": # for converting a single .py file
        source_files = os.path.join(input_dir, item_selected)
        output_file_path = ""

        if not os.path.exists(os.path.join(input_dir, "graph_output")):
            new_graph_output_folder = os.mkdir(os.path.join(input_dir, "graph_output"))
            output_file_path = os.path.join(input_dir, "graph_output", "{}_graph.png".format(item_selected.split(".")[0]))
        else:
            output_file_path = os.path.join(input_dir, "graph_output", "{}_graph.png".format(item_selected.split(".")[0]))
        
        graph_gen_instance = code2flow.code2flow(source_files, output_file=output_file_path, hide_legend=False, no_trimming=True)
        success_output_banner = st.success("Graph output has been successfully downloaded in {}".format(output_file_path))
        final_output_dict = {"graph_op": success_output_banner, "flag": 1, "output_image_path": output_file_path}
        return final_output_dict
    
    elif item_selected == None:
        error_output_banner = st.error("Please select a file to generate the graph.")
        final_output_dict = {"graph_op": error_output_banner, "flag": 0}
        return final_output_dict

#=============== Image display content ===============
def image_display(image_path):
    # view_image_button = st.button("View downloaded image")
    # print("============= view image ====> {}".format(view_image_button))
    # if view_image_button:
        # print("============= graph op ====> {}".format(graph_op['output_image_path']))
    image = Image.open(image_path)
    display_image = st.image(image, caption="Graph for the respective folder")
    return display_image
#=============== Image display content ===============

#============================ Code graph and code comment functions ============================

#============================ Code chunking functions ============================
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
#============================ Code chunking functions ============================

# Set the page to full screen
st.set_page_config(layout="wide")

# Set your OpenAI API key here
openai.api_key = "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"


# Streamlit UI components
st.title("Gen AI - Programming language interpreter")

# Dropdown for selecting programming language
programming_language = st.selectbox("Select Programming Language", ["Python", "SQL", "Java", "C++", "JavaScript", "PySpark"])

#=============== Folder/file input --- code graph ---- segment ===============

#base folder to store code folders
base_folder = "code_folders"

# Action - Option to create a new folder for uploading code files
with st.container():
    # Text input for entering the new folder name
    new_folder_name = st.text_input("Create a new folder:", placeholder="Enter folder name")
    # Button to create the new folder
    create_folder_button = st.button("Create Folder")
    if create_folder_button and new_folder_name:
        # Specify the path where you want to create the new folder
        folder_path = create_folder_in_base(new_folder_name)
        
# Get a list of folders in the base folder
folder_list = get_folder_list(base_folder)

# Action - File uploader section to upload a folder
selected_files_list = st.file_uploader("Upload your files", type=["py", "txt","zip"], accept_multiple_files=True, label_visibility="collapsed")

if selected_files_list:
     
    # Check if any of the selected files are zip files
    zip_files = [file for file in selected_files_list if file.name.endswith('.zip')]

    if zip_files:
        # Process each zip file one by one
        for zip_file in zip_files:
            process_zip_files(zip_file)
            
            # Remove the processed zip file from selected_files_list
            selected_files_list.remove(zip_file)
    # Check if selected_files_list is not empty after processing zip files
    if selected_files_list:
        # Dropdown to select a folder
        selected_folder_for_upload = st.selectbox("Select a folder to upload the file(s):", options=folder_list)

        # Upload(save) the selected files to chosen folder
        upload_selected_files(selected_files_list,selected_folder_for_upload)

# Get a list of folders in the base folder
# folder_list = [folder for folder in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, folder))]
folder_list = get_folder_list(base_folder)
selected_folder_for_display = ""
if isinstance(folder_list, list):
    selected_folder_for_display = st.selectbox("Select a folder to display:", options=["Select a folder"]+folder_list)

if selected_folder_for_display != "Select a folder" and selected_folder_for_display != "":
    #if selected_files_list:
    all_folder_files = get_files_from_folder(selected_folder_for_display)
    selected_file = get_selected_file(all_folder_files)

    # Creating 3 buttons for generating graph from folder, graph from a file and generating code comments
    scenario_1_button = st.button("Generate graph for the selected folder")
    # print("============= button check ====> {}".format(scenario_1_button))
    if scenario_1_button:
        graph_op = generate_graph(all_folder_files, os.path.join(base_folder, selected_folder_for_display))
        final_image_display = image_display(graph_op["output_image_path"])

        # if isinstance(graph_op, dict) and graph_op["flag"] == 1:
        # view_image_button = st.button("View downloaded image")
        # print("============= view image ====> {}".format(view_image_button))
        # if view_image_button:
        #     print("============= graph op ====> {}".format(graph_op['output_image_path']))
        #     image = Image.open(graph_op["output_image_path"])
        #     st.image(image, caption="Graph for the respective folder")
    
    scenario_2_button = st.button("Generate graph for the selected file")
    if scenario_2_button:
        graph_op = generate_graph(selected_file, os.path.join(base_folder, selected_folder_for_display))
        final_image_display = image_display(graph_op["output_image_path"])
        # print("================ checking graph output ====> {}".format(graph_op))

#=============== Folder/file input --- code graph ---- segment ===============


#=============== Code comment --- code chunkin ---- segment ===============    
    # File uploader for code
    # uploaded_file = st.file_uploader("Upload a .txt or .py file", type=["txt", "py"])

    # Create a folder to store code chunks
    if not os.path.exists(os.path.join(base_folder, selected_folder_for_display, "code_chunks")):
        os.makedirs(os.path.join(base_folder, selected_folder_for_display, "code_chunks"))

    scenario_3_button = st.button("Generate code comments for the selected file")
    if scenario_3_button and isinstance(selected_file, str) and selected_file != None:
        uploaded_file = os.path.join(base_folder, selected_folder_for_display, selected_file)
        # Create two sections using columns
        left_column, right_column = st.columns(2)
        # Read the uploaded file
        importing_file = open(uploaded_file, 'r')
        code_content = importing_file.read() #.decode("utf-8")
        left_text_area = left_column.text_area("INPUT CODE", code_content, height=400)

        token_limit = 1500 # Token limit for chunking
        # Check if the code has fewer than 20 lines, if so, don't chunk.

        if code_content.count('\n') < 20:
            chunks = [code_content]
        else:
            # Split the code into meaningful chunks.
            chunks = get_code_chunks(code_content, programming_language)

        # Generate comments for each chunk and store in files
        comments = []
        output_chunks = []

        # st.write("Chunks count : ", len(chunks))
        # st.write("##################################################################################")
        for i, chunk in enumerate(chunks):
            chunk_tokens = estimate_tokens(chunk)
            # st.write("Chunk :", i+1)
            # st.write("chunk_tokens : ", chunk_tokens)
            # st.write(chunk)
            if chunk_tokens is not None:
                # Check if the chunk exceeds the token limit
                if chunk_tokens >= token_limit:
                    large_chunks = chunk_large_code(chunk)
                    # st.write("large_chunks : ")
                    # st.write(large_chunks)
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
                        chunk_filename = os.path.join(base_folder, selected_folder_for_display, "code_chunks",
                                                      f"{os.path.splitext(selected_file)[0]}_chunk_{i + 1}_{j + 1}.txt")
                        with open(chunk_filename, "w") as chunk_file:
                            chunk_file.write(large_chunk)

                        # Display the generated comments
                        comments = response.choices[0].text
                        # st.write("Comments_2 : ")
                        # st.write(comments)
                        # st.write("##################################################################################")
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
                    chunk_filename = os.path.join(base_folder, selected_folder_for_display, "code_chunks",
                                                  f"{os.path.splitext(selected_file)[0]}_chunk_{i + 1}.txt")
                    with open(chunk_filename, "w") as chunk_file:
                        chunk_file.write(chunk)

                    # Display the generated comments
                    comments = response.choices[0].text
                    # st.write("Comments : ")
                    # st.write(comments)
                    # st.write("##################################################################################")
                    output_chunks.append(comments)

        # Merge the output chunks back into the original structure
        merged_code = "\n".join(output_chunks)
        output_filename = os.path.join(base_folder, selected_folder_for_display, "code_chunks",
                                                  f"{os.path.splitext(selected_file)[0]}_Output.txt")
        with open(output_filename, "w") as output_file:
            output_file.write(merged_code)

        # Display the chunked code and comments
        right_text_area = right_column.text_area("OUTPUT", merged_code, height=400)



    elif scenario_3_button and selected_file == None:
        st.error("Please select a file to proceed.")
    
#=============== Code comment --- code chunkin ---- segment ===============    
