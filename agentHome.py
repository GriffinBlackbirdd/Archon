from archonAgents.caseEvaluation import caseEvaluationAG
from archonAgents.documentReview import documentReviewAG
from archonAgents.legalAnalysis import legalAnalysisAG
from archonAgents.mcpAgents import mcpAgent
import asyncio
def main():
    print('''
1. Legal Analysis Agent
2. Document Review Agent
3. Case Evaluation Agent
4. Quick Summary Agent
''')

    try:
        option = int(input("Choose one: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return

    if option == 1:
        prompt = input("Enter your prompt: ")
        legalAnalysisAG(prompt)
    elif option == 2:
        prompt = input("Enter your prompt: ")
        documentReviewAG(prompt)
    elif option == 3:
        prompt = input("Enter your prompt: ")
        caseEvaluationAG(prompt)
    elif option == 4:
        prompt = input("Enter your prompt: ")
        asyncio.run(mcpAgent("I want a legal summary for the OQ agreement file."))
    else:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()