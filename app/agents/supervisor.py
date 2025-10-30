from langchain.tools import tool
from langchain.agents import create_agent

from app.util.config import config
from app.models.agent import PromptAnalysis
from app.agents.core.llm_factory import get_llm
from app.agents.analysis import analyser
from app.agents.research import researcher

SUPERVISOR_PROMPT = (
    "You are a supervisor with a team of agents exposed as tools."
    "Your task is to extract useful information from user input and find and upload country-specific GHG conversion factors data."
    "To do this, perform the following tasks in order, calling the relevant tools:"
    "   1. Prompt Analysis: Extract country code and year from input prompt."
    "       - Tool should return a country code and year in YYYY format."
    "       - If either field is empty or contains the text 'Invalid', terminate the workflow with message 'Invalid Inputs.'."
    "   2. Research: Search online for download links based on the data found in step 1."
    "Return final response received from tool as-is without any additional explanation or other text."
)

@tool("prompt_analysis",
      description="Use this tool to call an agent that analyses user input prompt.")
def prompt_analysis(user_prompt:str) -> PromptAnalysis:
    """Analyses input prompt and extracts country code and year."""
    result = analyser.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        })
    return result["structured_response"]

@tool("research",
      description="Use this tool to call an agent that searches online for GHG conversion factor download links.")
def research(country_code:str, year:str) -> str:
    """Finds GHG conversion factors data download links online."""
    result = researcher.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": PromptAnalysis(CountryCode=country_code, Year=year).model_dump_json()
                }
            ]
    })
    return result["messages"][-1].content

supervisor = create_agent(name="Supervisor",
                        model=get_llm(),
                        tools=[prompt_analysis, research],
                        system_prompt=SUPERVISOR_PROMPT)