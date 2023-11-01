import streamlit as st

# Set the page to full screen
st.set_page_config(layout="wide")

# Set the page title
st.title("AICOE - GEN AI CODE INTERPRETER")

# Dropdown list with 5 options
selected_option = st.selectbox("Select a programming language", ["PYTHON", "SQL", "JAVA", "C", "C++"])

# Create two sections using columns
left_column, right_column = st.columns(2)

left_text = left_column.text_area("Input text area", "", height=400)

# Text area on the right
right_text = right_column.text_area("OUTPUT", "", height=400)


# Submit button
if left_column.button("Submit"):
    right_column.write(f"You selected: {selected_option}")
    
