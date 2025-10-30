from pydantic import BaseModel, Field

class PromptAnalysis(BaseModel):
    country_code:str = Field(alias="CountryCode",
                             description="ISO-3166-2 country code or 'Invalid' if input has invalid coyntry name.")
    year:str = Field(alias="Year",
                     description="Year in YYYY format.")