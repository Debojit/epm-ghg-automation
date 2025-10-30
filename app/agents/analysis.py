from datetime import datetime

from langchain.agents import create_agent
from langchain.tools import tool

from app.agents.core.llm_factory import get_llm
from app.models.agent import PromptAnalysis

ANALYSER_PROMPT = (
    "You are a prompt analysis assistant."
    "Analyse the user input and extract the country name and year from it."
    "If needed, convert the country name to the ISO-3166-2 country code."
    "Input year is to be converted to YYYY format if needed."
    "If input year is missing in the user prompt, check current date & time. If current month is after 'June', then return current year in YYYY format, else return previous year in YYYY format."
)

@tool("current_datetime", description="Use this tool to get the current date & time.")
def get_current_datetime():
    """Returns current date & time."""
    return datetime.now()

analyser = create_agent(name="Prompt Analyser",
                        model=get_llm(),
                        tools=[get_current_datetime],
                        response_format=PromptAnalysis,
                        system_prompt=ANALYSER_PROMPT)