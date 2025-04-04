from archonAgents.caseEvaluation import caseEvaluationAG
from archonAgents.documentReview import documentReviewAG
from archonAgents.legalAnalysis import legalAnalysisAG
from archonAgents.mcpAgents import mcpAgent
import asyncio
import os
import sys


def read_file_content(file_path):
    """
    Read and return the content of a file based on its extension.
    Supports .txt, .pdf, .doc, and .docx files.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return None

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif file_extension == ".pdf":
        try:
            import PyPDF2

            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text() + "\n"
                return text
        except ImportError:
            print(
                "Error: PyPDF2 module not found. Install it using 'pip install PyPDF2'"
            )
            return None
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            return None

    elif file_extension in [".doc", ".docx"]:
        try:
            import docx

            doc = docx.Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])
            return content
        except ImportError:
            print(
                "Error: python-docx module not found. Install it using 'pip install python-docx'"
            )
            return None
        except Exception as e:
            print(f"Error reading Word file: {e}")
            return None

    else:
        print(f"Unsupported file format: {file_extension}")
        return None


def main():
    print("""
1. Legal Analysis Agent
2. Document Review Agent
3. Case Evaluation Agent
4. Quick Summary Agent
""")

    try:
        option = int(input("Choose one: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    if option in [1, 2, 3]:
        prompt = input("Enter your prompt: ")
        file_path = input("Enter file path (optional, press enter to skip): ").strip()

        content = None
        if file_path:
            content = read_file_content(file_path)
            if content is None:
                retry = input("Do you want to continue without a file? (y/n): ")
                if retry.lower() != "y":
                    return

        # Call the appropriate agent based on the option
        if option == 1:
            if content:
                legalAnalysisAG(prompt, content)
            else:
                legalAnalysisAG(prompt)
        elif option == 2:
            if content:
                documentReviewAG(prompt, content)
            else:
                documentReviewAG(prompt)
        elif option == 3:
            if content:
                caseEvaluationAG(prompt, content)
            else:
                caseEvaluationAG(prompt)

    elif option == 4:
        prompt = input("Enter your prompt: ")
        asyncio.run(mcpAgent("I want a legal summary for the OQ agreement file."))

    else:
        print("Please enter a valid number.")


if __name__ == "__main__":
    main()
