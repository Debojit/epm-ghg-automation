from datetime import datetime

from langchain.agents import create_agent
from langchain.tools import tool

from app.agents.core.llm_factory import get_llm
from app.models.agent import PromptAnalysis

ANALYSER_PROMPT = (
    "You are a prompt analysis assistant."
    "Analyse the user input and extract the country name and year from it."
    "Convert the country name to the ISO-3166-2 country code if needed."
    "If year is missing in the user prompt, check current date. If current month is after 'June', then return current year in YYYY format, else return the previous year in YYYY format."
    "Convert the year to YYYY format if needed."
)

@tool("current_datetime",
      description="Use this tool to get the current date in YYYY-MM-DD format.")
def get_current_date() -> str:
    """Returns current date & time."""
    return datetime.now().strftime("%Y-%m-%d")

analyser = create_agent(name="Prompt Analyser",
                        model=get_llm(),
                        tools=[get_current_date],
                        response_format=PromptAnalysis,
                        system_prompt=ANALYSER_PROMPT)