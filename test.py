from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.yaml import YamlStorage
from agno.models.google import Gemini
from dotenv import load_dotenv
from agno.tools.exa import ExaTools

load_dotenv()

agent = Agent(
    model=Gemini("gemini-2.0-flash", api_key="AIzaSyCWznUz8cnPCkzJ6Bu9ikQGWF6kc-ZUu9k"),
    storage=YamlStorage(dir_path="agent_sessions_yaml"),
    tools=[ExaTools(answer=True)],
    add_history_to_messages=True,
)

agent.print_response("What is the capital of India?")
agent.print_response("What is so special about this city?")
