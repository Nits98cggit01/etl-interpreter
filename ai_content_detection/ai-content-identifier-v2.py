import openai

# Define your OpenAI API key
openai.api_key = "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"

# Input paragraph
input_paragraph = """
Education is one of the most important means of empowering women with the knowledge, skills, and self-confidence necessary to participate fully in the development process. Governments should establish mechanisms to accelerate women’s equal participation and equitable representation at all levels of the political process and public life in each community and society and enable women to articulate their concerns and needs and ensure the full and equal participation of women in decision-making processes in all spheres of life. Governments and civil society should take actions to eliminate attitudes and practices that discriminate against girls and women and gender inequality, will be able to complete a full course of primary schooling and that girls and boys will have equal access to all levels of education. Women are facing threats to their lives, health, and well-being as a result of being overburdened with work and of their lack of power and influence. In most regions of the world, women receive less formal education than men, and at the same time, abilities and coping mechanisms often go unrecognized. The power relations that women's attainment of healthy and fulfilling lives operate at many levels of society, from the most personal to the highly public. Achieving change requires policy and programme actions that will improve women's access to secure livelihoods and economic resources, alleviate their extreme responsibilities with regard to housework, remove legal to their participation in public life, and raise social awareness through effective programmes of education and mass communication.
"""

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
    prompt=input_paragraph,
    max_tokens=1024,  # Adjust max tokens based on your requirement
    stop=None,
    temperature=0.2,  # Set temperature to 0 for deterministic output
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Extract the AI-generated content from the response
ai_generated_content = response.choices[0].text.strip()

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
print(highlighted_content)
