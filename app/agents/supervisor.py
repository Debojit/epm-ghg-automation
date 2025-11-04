from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from app.models.agent import PromptAnalysis, WorkflowContext
from app.models.conversion_factors import ConversionFactor
from app.agents.core.llm_factory import get_llm
from app.agents.analysis import analyser
from app.agents.research import researcher
from app.agents.acquisition import acquirer
from app.util.logging import get_logger

SUPERVISOR_PROMPT = (
    "You are a supervisor with a team of agents exposed as tools."
    "Your task is to extract useful information from user input and find and upload country-specific GHG conversion factors data."
    "To do this, perform the following tasks in order, calling the relevant tools:"
    "   1. Prompt Analysis: Extract country code and year from input prompt."
    "       - Tool should return a country code and year in YYYY format."
    "       - If either field is empty or contains the text 'Invalid', terminate the workflow with message 'Invalid Inputs.'."
    "   2. Research: Search online for download links based on the data found in step 1."
    "   3. Acquistion: Acquire and normalise data from the download link found in step 2."
    "   4. Data Load: Load the normalised data from step 3 into Oracle EPM."
    "Return final response received from tool as-is without any additional explanation or other text."
)

logger = get_logger(__name__)


@tool(
    "prompt_analysis",
    description="Use this tool to call an agent that analyses user input prompt.",
)
def prompt_analysis(
    user_prompt: str, runtime: ToolRuntime[WorkflowContext]
) -> PromptAnalysis:
    """Analyses input prompt and extracts country code and year."""
    logger.info(f"Analysing user prompt:'{user_prompt}'")

    result = analyser.invoke(
        {"messages": [HumanMessage(user_prompt)]}, context=runtime.context
    )

    analysis: PromptAnalysis = result["structured_response"]
    runtime.context.country_code = analysis.country_code
    runtime.context.year = analysis.year

    logger.info(f"Found Country Code:{analysis.country_code}, Year:{analysis.year}")
    return analysis


@tool(
    "research",
    description="Use this tool to call an agent that searches online for GHG conversion factor download links.",
)
def research(runtime: ToolRuntime[WorkflowContext]) -> str:
    """Finds GHG conversion factors data download links online."""
    logger.info(
        f"Looking for GHG conversions factor document for {runtime.context.country_code} in {runtime.context.year}."
    )

    result = researcher.invoke(
        {
            "messages": [
                HumanMessage(
                    f"Country Code:{runtime.context.country_code}, Year:{runtime.context.year}"
                )
            ]
        },
        context=runtime.context,
    )
    doc_url = result["messages"][-1].content
    runtime.context.doc_url = doc_url

    logger.info(f"Found document URL: {doc_url}")
    return doc_url


@tool(
    "acquisition",
    description="Use this tool to download and transform country-specific GHG conversion factors data into a normalised format.",
)
def acquisition(runtime: ToolRuntime[WorkflowContext]) -> list[ConversionFactor]:
    """Downloads and transforms GHG conversion factors data."""
    logger.info(
        f"Attempting to extract data from document at {runtime.context.doc_url}."
    )

    result = acquirer.invoke(
        {
            "messages": [
                HumanMessage(
                    f"Download and normalise the data for the document located at {runtime.context.doc_url}."
                )
            ]
        }
    )
    ghg_data: list[ConversionFactor] = result["messages"][-1].content

    return ghg_data


@tool("data_load", description="Use this tool to load normlaised data into Oracle EPM.")
def data_load(ghg_data: list[ConversionFactor]):
    import pprint

    pprint.pp(ghg_data, indent=4, width=100)


supervisor = create_agent(
    name="Supervisor",
    model=get_llm(),
    context_schema=WorkflowContext,
    tools=[prompt_analysis, research, acquisition, data_load],
    system_prompt=SUPERVISOR_PROMPT,
)
