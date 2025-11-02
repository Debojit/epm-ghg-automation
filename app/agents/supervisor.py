from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from app.models.agent import PromptAnalysis, WorkflowContext
from app.agents.core.llm_factory import get_llm
from app.agents.analysis import analyser
from app.agents.research import researcher
from app.util.logging import get_logger

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

logger = get_logger(__name__)

@tool("prompt_analysis",
      description="Use this tool to call an agent that analyses user input prompt.")
def prompt_analysis(user_prompt:str, runtime:ToolRuntime[WorkflowContext]) -> PromptAnalysis:
    """Analyses input prompt and extracts country code and year."""
    logger.info(f"Analysing user prompt:'{user_prompt}'")

    result = analyser.invoke({"messages": [HumanMessage(user_prompt)]},
            context=runtime.context)
    
    analysis:PromptAnalysis = result["structured_response"]
    runtime.context.country_code = analysis.country_code
    runtime.context.year = analysis.year
    
    logger.info(f"Found Country Code:{analysis.country_code}, Year:{analysis.year}")
    return analysis

@tool("research",
      description="Use this tool to call an agent that searches online for GHG conversion factor download links.")
def research(runtime:ToolRuntime[WorkflowContext]) -> str:
    """Finds GHG conversion factors data download links online."""
    logger.info(f"Looking for GHG conversions factor document for {runtime.context.country_code} in {runtime.context.year}.")
    
    result = researcher.invoke({
            "messages": [HumanMessage(f"Country Code:{runtime.context.country_code}, Year:{runtime.context.year}")]},
            context=runtime.context)
    doc_url = result["messages"][-1].content
    runtime.context.doc_url = doc_url

    logger.info(f"Found document URL: {doc_url}")
    return doc_url

supervisor = create_agent(name="Supervisor",
                        model=get_llm(),
                        context_schema=WorkflowContext,
                        tools=[prompt_analysis, research],
                        system_prompt=SUPERVISOR_PROMPT)