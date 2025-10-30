from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    APPLICATION_NAME:str = ""
    
    #LLM Config
    LLM_API_KEY:str = ""
    MODEL_NAME:str = ""
    MODEL_TEMPERATURE:float = 0.0

    # Tool Config
    SERPER_API_KEY:str = ""
    FIRECRAWL_API_KEY:str = ""

config = Config()