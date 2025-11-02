from langchain.messages import HumanMessage

from app.agents.supervisor import supervisor

def test_valid_input():
    """
    Test if the agent workflow is performing normally with valid inputs.

    Inputs:
        Country: United Kingdom
        Year: 2025
    Expected: Conversion factors download link.
    """
    result = supervisor.invoke({
            "messages": [HumanMessage("Please find GHG conversion factors for the United Kingdom in 2025")]
        })
    assert result["messages"][-1] not in (None, "")

def test_invalid_country():
    """
    Test if the agent workflow is performing normally with valid inputs.

    Inputs:
        Country: Wakanda
        Year: 2025
    Expected: "Invalid Inputs."
    """
    result = supervisor.invoke({
            "messages": [HumanMessage("Please find GHG conversion factors for the Wakanda in 2025.")]
        })
    assert result["messages"][-1].content == "Invalid Inputs."

def test_invalid_year():
    """
    Test if the agent workflow is performing normally with valid inputs.

    Inputs:
        Country: United Kingdom
        Year: 1800
    Expected: "Invalid Inputs."
    """
    result = supervisor.invoke({
            "messages": [HumanMessage("Please find GHG conversion factors for the United Kingdom in 1800")]
        })
    assert result["messages"][-1].content == "Invalid Inputs."