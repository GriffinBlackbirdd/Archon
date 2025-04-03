# from archonAgents.caseEvaluation import caseEvaluationAG
# from archonAgents.documentReview import documentReviewAG
# from archonAgents.legalAnalysis import legalAnalysisAG

# def main():
#     print('''
# 1. Legal Analysis Agent
# 2. Document Review Agent
# 3. Case Evaluation Agent
# ''')

#     try:
#         option = int(input("Choose one: "))
#     except ValueError:
#         print("Invalid input! Please enter a number.")
#         return

#     if option == 1:
#         prompt = input("Enter your prompt: ")
#         legalAnalysisAG(prompt)
#     elif option == 2:
#         prompt = input("Enter your prompt: ")
#         documentReviewAG(prompt)
#     elif option == 3:
#         prompt = input("Enter your prompt: ")
#         caseEvaluationAG(prompt)
#     else:
#         print("Please enter a valid number.")

# if __name__ == "__main__":
#     main()

import os
import json
import spacy
from archonAgents.caseEvaluation import caseEvaluationAG
from archonAgents.documentReview import documentReviewAG
from archonAgents.legalAnalysis import legalAnalysisAG

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def extract_filename(prompt):
    doc = nlp(prompt)
    for ent in doc.ents:
        if ent.label_ in ["WORK_OF_ART", "ORG", "PRODUCT"]:
            return ent.text
    return None

def find_file(filename, directory="."):
    for root, _, files in os.walk(directory):
        for file in files:
            if filename.lower() in file.lower():
                return os.path.join(root, file)
    return None

def process_prompt(prompt):
    filename = extract_filename(prompt)
    if filename:
        file_path = find_file(filename)
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            # Store file path and prompt in JSON
            log_data = {"prompt": prompt, "file_path": file_path}
            with open("file_logs.json", "w", encoding="utf-8") as log_file:
                json.dump(log_data, log_file, indent=4)
            return prompt + "\n\n" + file_content
    return prompt

def main():
    print('''\n1. Legal Analysis Agent\n2. Document Review Agent\n3. Case Evaluation Agent\n''')

    try:
        option = int(input("Choose one: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    prompt = input("Enter your prompt: ")
    updated_prompt = process_prompt(prompt)

    if option == 1:
        legalAnalysisAG(updated_prompt)
    elif option == 2:
        documentReviewAG(updated_prompt)
    elif option == 3:
        caseEvaluationAG(updated_prompt)
    else:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
