import requests

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

from app.models.agent import WorkflowContext
from app.models.conversion_factors import ConversionFactor
from app.agents.core.llm_factory import get_llm
from app.agents.transformers.registry import registry

ACQUISITION_PROMPT = (
    "You are a document acquisition and data transformation specialist."
    "You will be provided the download URL for a country-specific GHG conversion factors data document."
    "Perform these actions with the URL:"
    "1. Download the document indicated by the URL with the downloader tool and store the file locally."
    "2. Transform the document's data into a common format for later use."
    "3. Return the data thus transformed."
)


@tool(
    "download_file",
    description="Use this tool to download the file from the URL provided, store it locally, then return the path.",
)
def download_file(url: str) -> str:
    """Download a remote file based on URL input."""
    local_filename = f"/tmp/{url.split('/')[-1]}"

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

@tool(
    "transform_data",
    description="Use this tool to transform the country-specific GHG conversion factors document into a normalised format."
)
def transform_data(file_path:str, runtime:ToolRuntime[WorkflowContext]):
    """Convert country-specific file data into normalised form."""
    transformer = registry.get(runtime.context.country_code.lower())
    ghg_data = transformer(file_path)

acquirer = create_agent(
    name="Data Acquirer",
    model=get_llm(),
    context_schema=WorkflowContext,
    tools=[download_file],
    system_prompt=ACQUISITION_PROMPT,
)
