from pathlib import Path
from textwrap import dedent
from dotenv import load_dotenv
import asyncio

load_dotenv()
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters


async def mcpAgent(message: str) -> None:
    root_dir = Path("/Users/eagle/Developer/archon/archonX/archon/docs/")
    server_params1 = StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            str(root_dir),
        ],
    )

    # Set up the second MCP server (hypothetical example, replace with actual second tool)
    server_params2 = StdioServerParameters(
        command="node",
        args=[
            "/Users/eagle/Developer/archon/archonX/archon/mcp-cerebra-legal-server/build/index.js"
        ],
        disabled=False,
    )

    # Create MCPTools instances for both servers
    async with (
        MCPTools(server_params=server_params1) as mcp_tools1,
        MCPTools(server_params=server_params2) as mcp_tools2,
    ):
        agent = Agent(
            model=Gemini("gemini-2.0-flash"),
            tools=[mcp_tools1, mcp_tools2],
            instructions=dedent("""
                You are an assistant with access to two tools: a filesystem tool and a Legal Assitant tool.
                Use the filesystem tool to find the file and read it's content, then use that information
                with the second tool to perform further actions.

                - First, use the filesystem tool to navigate and find relevant files
                - Then, use the content or information from those files with the second tool to provide legal advise
                - Provide clear explanations of your actions and findings
                - Be concise and focus on relevant information
            """),
            markdown=True,
            show_tool_calls=True,
        )

        # Run the agent
        # await agent.aprint_response(message, stream = True)
        result = await agent.arun(message)
        print(result.content)


# if __name__ == "__main__":
#     asyncio.run(mcpAgent("I want a legal summary for the OQ agreement file."))
