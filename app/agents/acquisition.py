import os
import uuid
from pathlib import Path

import requests

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

from app.models.agent import WorkflowContext
from app.models.conversion_factors import ConversionFactor
from app.agents.core.llm_factory import get_llm
from app.agents.transformers.registry import registry

registry.discover()

ACQUISITION_PROMPT = (
    "You are a document acquisition and data transformation specialist."
    "You will be provided the download URL for a country-specific GHG conversion factors data document."
    "Download and transform the data into a normalised form using the 'acquire_data' tool."
    "Return the transformed data."
)


def _download_file(url: str) -> Path:
    """Download a remote file based on URL input."""
    local_file_path = Path("/tmp") / f"{uuid.uuid4()}_{Path(url).name}"
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            f.flush()
            os.fsync(f.fileno())
    return local_file_path


def _transform_data(country_code: str, local_file_path: Path) -> list[ConversionFactor]:
    """Convert country-specific file data into normalised form."""
    transformer = registry.get(country_code.lower())
    ghg_data = transformer(local_file_path)
    os.remove(local_file_path)
    return ghg_data


@tool(
    "acquire_data",
    description="Use this tool to download and transform the GHG conversion factors data.",
)
def acquire_data(runtime: ToolRuntime[WorkflowContext]) -> list[ConversionFactor]:
    """Acquire and transform GHG conversion factors data."""
    local_file_path = _download_file(runtime.context.doc_url)
    ghg_data = _transform_data(runtime.context.country_code, local_file_path)

    return ghg_data


acquirer = create_agent(
    name="Data Acquirer",
    model=get_llm(),
    context_schema=WorkflowContext,
    tools=[acquire_data],
    system_prompt=ACQUISITION_PROMPT,
)
