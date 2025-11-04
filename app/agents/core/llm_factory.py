from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.util.config import config


def get_llm():
    llm = ChatOpenAI(
        api_key=SecretStr(config.LLM_API_KEY),
        model=config.MODEL_NAME,
        temperature=config.MODEL_TEMPERATURE,
    )
    return llm
