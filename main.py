from pydantic import BaseModel, Field
from typing import List
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.exa import ExaTools
from PyPDF2 import PdfReader
from dotenv import load_dotenv
load_dotenv()

class TradeLegalParams(BaseModel):
    reply: str = Field(..., description="Provide the reply to the question asked by the user if it's trade related.")
    cons: str = Field(..., description="Provide all the cons in the trade legal contract.")
    laws: str = Field(..., description="Provide all the laws that are being broken, if any exists.")
    betterment: str = Field(..., description="Suggest what better can be done in the trade legal contract.")

tradeAgent = Agent(
    name="Trade contract analyzer",
    model=Gemini("gemini-2.0-flash"),
    tools = [ExaTools(answer = True, highlights = True)],
    # response_model=TradeLegalParams,
    role="You are a legal expert. You will be provided with a trade legal contract. You need to analyze the contract and provide the cons, laws that are being broken, if any exists, and suggest what better can be done in the trade legal contract.",
)
consultancyAgent = Agent(
    name = "Consultancy agent",
    model = Gemini("gemini-2.0-flash"),
    tools = [ExaTools(answer = True, highlights = True)],
    # response_model=TradeLegalParams,
    role = "You are a consultancy expert, you will be provided with a contract. You need to analyze the contract and provide the cons, laws that are being broken, if any exists, and suggest what better can be done in the contract.",
)

def read_pdf_content(pdf_path: str) -> str:

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
pdf_path = "/Users/eagle/Developer/archon/archon/docs/OQ Agreement.pdf"
pdf_content = read_pdf_content(pdf_path)

team = Team(
    name="Legal Research Team",
    mode="route",
    model=Gemini("gemini-2.0-flash"),
    members=[tradeAgent, consultancyAgent],
    markdown=True,
)
team.print_response(pdf_content)