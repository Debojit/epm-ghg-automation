from pydantic import BaseModel, Field


class PromptAnalysis(BaseModel):
    country_code: str = Field(
        alias="CountryCode",
        description="ISO-3166-2 country code or 'Invalid' if input has invalid coyntry name.",
    )
    year: str = Field(alias="Year", description="Year in YYYY format.")


class WorkflowContext(BaseModel):
    user_prompt: str = Field(
        alias="UserPrompt",
        description="Initial prompt supplied by the user.",
        default="",
    )
    country_code: str = Field(
        alias="CountryCode",
        description="ISO-3166-2 country code or 'Invalid' if input has invalid coyntry name.",
        default="",
    )
    year: str = Field(alias="Year", description="Year in YYYY format.", default="")
    doc_url: str = Field(
        alias="DocUrl",
        description="Download URL for the GHG conversions factor document.",
        default="",
    )
    local_file_path: str = Field(
        alias="LocalFilePath",
        description="Absolute local path to the file stored locally.",
        default="",
    )
