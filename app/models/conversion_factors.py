from pydantic import BaseModel, Field


class ConversionFactor(BaseModel):
    car_type: str = Field(
        alias="CarType",
        description="Type of car for which GHG conversion factors are to be loaded.",
    )
    total_kg_co2e: float = Field(
        alias="KgCo2e",
        description="The total CO2 equivalent emission factor for the activity.",
    )
    kg_co2e_of_co2: float = Field(
        alias="KgCo2eOfCo2",
        description="The portion of the factor from CO2 emissions, expressed as kg CO2e.",
    )
    kg_co2e_of_ch4: float = Field(
        alias="KgCo2eOfCh4",
        description="The portion of the factor from CH4 emissions, expressed as kg CO2e.",
    )
    kg_co2e_of_n2o: float = Field(
        alias="KgCo2eOfN2o",
        description="The portion of the factor from N2O emissions, expressed as kg CO2e.",
    )
