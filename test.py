from agno.agent import Agent
from agno.tools.googlecalendar import GoogleCalendarTools
import datetime
import os
from agno.models.google import Gemini
from tzlocal import get_localzone_name
from dotenv import load_dotenv

load_dotenv()
agent = Agent(
    name="Google Calendar Assistant",
    model=Gemini("gemini-2.0-flash"),
    tools=[
        GoogleCalendarTools(
            credentials_path="/Users/eagle/Developer/archon/archonX/archon/client_secret_997385589848-oti9ok7j8c1c6arg9u93t9p97jo76oad.apps.googleusercontent.com.json"
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

agent.print_response("Give me the list of todays events", markdown=True)
