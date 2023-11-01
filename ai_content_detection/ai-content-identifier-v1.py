# import spacy

# # Load the English language model from spaCy
# nlp = spacy.load("en_core_web_sm")

# def linguistic_analysis(paragraph):
#     # Process the input paragraph with spaCy
#     doc = nlp(paragraph)

#     # Analyze word complexity and idiomatic expressions
#     complexity_score = sum([1 for token in doc if token.is_alpha and len(token.text) > 5])
#     idiomatic_score = sum([1 for token in doc if token.text.lower() in idiomatic_phrases])

#     # Analyze grammatical errors
#     grammatical_errors = [token.text for token in doc if token.dep_ == "punct"]

#     # Analyze sentence structure
#     sentence_structure = [len(sent) for sent in doc.sents]

#     return {
#         "Complex Words": complexity_score,
#         "Idiomatic Phrases": idiomatic_score,
#         "Grammatical Errors": grammatical_errors,
#         "Sentence Structure": sentence_structure,
#     }

# # Example paragraph for analysis
# example_paragraph = "Despite the inclement weather, the conference proceeded as scheduled. However, the AI-generated content showed significant complexity and a paucity of idiomatic expressions."

# # Example idiomatic phrases
# idiomatic_phrases = ["proceeded as scheduled", "inclement weather", "showed significant"]

# analysis_result = linguistic_analysis(example_paragraph)
# print("Linguistic Analysis Results:")
# print(analysis_result)

import openai

# Define your OpenAI GPT-3 API key
api_key = "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"

# Function to find grammatical errors using GPT-3
def find_grammatical_errors(prompt, api_key):
    openai.api_key = api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,  # Adjust as needed
        temperature=0.2,  # Adjust for creativity vs. accuracy
    )

    return response.choices[0].text

paragraph = "The wait is finally over, 13th edition of ICC world cup has returned in all its glory to crown a new champion in the world of cricket.India hosts the 2023 world cup and it could not be a better time for the Indian fans to cheer for the boys in blue and enjoy the most celebrated sports in the country. World cup 23 will be witness of fierce battle and world class display of cricket across 48 matches among 10 competitive teams, each team playing 9 matches against the rest.The Total prize fund of world cup23 is $10 million, which is 74 crore and 15 lakhs rupees in Indian Currency. The team that wins the World Cup gets $4 million, the runner-up gets $2 million, and the teams that reach the semi-finals each receive $800,000. Teams also earn $40,000 for each match they win during the league stage. Even if a team doesn’t make it past the league stage, they still get $100,000. Look forward to world cup 23 starting from 5th Oct to 19th November."
prompt = f"Act as an english teacher. Your task is to identify the grammatical or punctuation errors in the following text. Make sure you display only the sentences with grammatical error with no explanation!! : '{paragraph}'"

result = find_grammatical_errors(prompt, api_key)

print("GPT-3's Suggestions:")
print(result)


