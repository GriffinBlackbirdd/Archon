from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.googlecalendar import GoogleCalendarTools
import datetime
import os
from tzlocal import get_localzone_name


def legalClock(prompt):
    agent = Agent(
        model=Gemini(
            "gemini-2.0-flash", api_key="AIzaSyCWznUz8cnPCkzJ6Bu9ikQGWF6kc-ZUu9k"
        ),
        tools=[
            GoogleCalendarTools(
                credentials_path="/Users/eagle/Developer/archon/archonX/archon/credentials.json",
                token_path="/Users/eagle/Developer/archon/archonX/archon/token.json",
            )
        ],
        show_tool_calls=True,
        instructions=[
            f"""
            You are scheduling assistant . Today is {datetime.datetime.now()} and the users timezone is {get_localzone_name()}.
            You should help users to perform these actions in their Google calendar:
                - get their scheduled events from a certain date and time
                - create events based on provided details
            """
        ],
        add_datetime_to_instructions=True,
    )
    response = agent.run(
        prompt
        + "timezone is Asia/Kolkata, set duration to 1 hour if not provided, and decide a title on your own if not provided",
    )
    return response.content
