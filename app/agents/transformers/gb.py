import json
from pathlib import Path

import pandas as pd
 
from langchain.agents import create_agent
from langchain.messages import HumanMessage

from app.agents.core.llm_factory import get_llm
from app.agents.transformers.registry import registry
from app.models.conversion_factors import ConversionFactor

PROMPT = (
    "You are a data transformation assistant for UK DEFRA GHG data. "
    "You will receive tabular data in dictionary form derived from a pandas DataFrame. "
    "Transform this data as follows:"
    "   1. Filter rows for 'Cars by Vehicle Size'."
    "   2. Include merged column headers such as 'Diesel', 'Petrol', etc., by combining them with the size field into the 'Type' column, e.g., 'Diesel - Small Car'."
    "   3. Only include rows where the unit of measure (UOM) is 'kilometers'."
    "   4. Default blank numeric fields to 0."
    "   5. For blank 'Type' fields, fill them with the previous row's 'Type' value."
    "   6. Modify the 'Type' column to abbreviations."
    "       e.g. Battery Electric Vehicles = BEV"
    "            Plug-in Hybrid Electric Vehicle = PEV"
    "   7. Omit the 'Activity' and 'Unit' columns from the final output."
    "Return the final result as a single JSON array of objects specified."
    "Do not omit any 'Type' field entry, even if all the conversion factor fields are empty."
    "Return all 'Type' field combinations, defaulting the empty conversion factors fields to 0."
    "The first character of your response must be '[' and the last must be ']'. "
    "Do not include any top-level keys such as 'data'. "
    "Do not include any explanations, markdown, or text outside the JSON array."
)

_transformer = create_agent(name="UK Data Transformer",
                              model=get_llm(),
                              system_prompt=PROMPT)

def transform_gb(file_path:Path) -> list[ConversionFactor]:
    ghg_df = pd.read_excel(file_path, sheet_name="Passenger vehicles")
    result = _transformer.invoke({"messages": [HumanMessage(ghg_df.to_csv())]})
    raw_data:str = result["messages"][-1].content
    clean_data = raw_data.replace("```json", "").replace("```", "")
    ghg_json = json.loads(clean_data)
    ghg_data = [ConversionFactor(CarType=record["Type"],
                    KgCo2e=record["kg CO2e"],
                    KgCo2eOfCo2=record["kg CO2e of CO2 per unit"],
                    KgCo2eOfCh4=record["kg CO2e of CH4 per unit"],
                    KgCo2eOfN2o=record["kg CO2e of N2O per unit"])
                for record in ghg_json]
    return ghg_data

registry.register("gb", transform_gb)