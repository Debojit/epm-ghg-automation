from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.document_loaders import FireCrawlLoader
from langchain_core.documents import Document
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent

from app.util.config import config
from app.agents.core.llm_factory import get_llm
from app.models.agent import WorkflowContext

RESEARCH_PROMPT = (
    "You are a researcher capable of searching for documents online."
    "You will be provided with a ISO-3166-2 country code and a year in YYYY format as input."
    "Using the input data, perform the following actions in order:"
    "1. Search online for pages with GHG Conversion factors for the provided country and year."
    "   - Prefer URLs from government websites of the country provided rather than other sources."
    "   - Return the page URL."
    "2. Crawl the URL page from step 1 and extract file download links for GHG conversion factors."
    "   - Return only the list of URLs for GHG conversion factors."
    "   - Prefer Excel file download links where available."
    "   - Only return non-Excel download links if Excel is not available."
    "   - If there are mutliple links, return the link to the document that appears to have the most data."
    "   - Return the response as a string containing only the URL."
    "   - If any of the inputs are invalid or a candidate URL cannot be found, return an empty text. No explanations necessary."
    "   - Just return the results; don't return any extra text."
)


@tool("web_search_serp", description="Use this tool to search for GHG factors online.")
def serp_tool(country_code: str, year: str) -> str:
    """Search online based on input parameters."""
    search = GoogleSerperAPIWrapper(
        gl=f"{country_code.lower()}", serper_api_key=config.SERPER_API_KEY
    )

    results = search.results(
        f"Find GHG conversion factors data for {country_code} in the year {year}"
    )
    urls = [item["link"] for item in results["organic"]]

    return urls[0]


@tool(
    "crawl_page",
    description="Use this tool to crawl the provided page contents as markdown.",
)
def crawler_tool(url: str) -> list[Document]:
    """Get page contents as markdown"""
    loader = FireCrawlLoader(api_key=config.FIRECRAWL_API_KEY, url=url, mode="scrape")
    return loader.load()


researcher = create_agent(
    name="Researcher",
    model=get_llm(),
    context_schema=WorkflowContext,
    tools=[serp_tool, crawler_tool],
    system_prompt=RESEARCH_PROMPT,
)
