from typing import Any

from langchain.messages import HumanMessage

from app.agents.supervisor import supervisor
from app.models.agent import WorkflowContext

def test_valid_input():
    """
    Test if the agent workflow is performing normally with valid inputs.

    Inputs:
        Country: United Kingdom
        Year: 2025
    Expected: Conversion factors download link.
    """
    user_prompt = "Please find GHG conversion factors for the United Kingdom in 2025"
    user_message = HumanMessage(user_prompt)
    context = WorkflowContext(UserPrompt=user_prompt)
    result = _invoke_agent(user_message, context)
    assert result["messages"][-1] not in (None, "")

def test_invalid_country():
    """
    Test if the agent workflow is performing normally with valid inputs.

    Inputs:
        Country: Wakanda
        Year: 2025
    Expected: "Invalid Inputs."
    """
    user_prompt = "Please find GHG conversion factors for the Wakanda in 2025."
    user_message = HumanMessage(user_prompt)
    context = WorkflowContext(UserPrompt=user_prompt)
    result = _invoke_agent(user_message, context)
    assert result["messages"][-1].content == "Invalid Inputs."

def test_invalid_year():
    """
    Test if the agent workflow is performing normally with valid inputs.

    Inputs:
        Country: United Kingdom
        Year: 1800
    Expected: "Invalid Inputs."
    """
    user_prompt = "Please find GHG conversion factors for the United Kingdom in 1800."
    user_message = HumanMessage(user_prompt)
    context = WorkflowContext(UserPrompt=user_prompt)
    result = _invoke_agent(user_message, context)
    assert result["messages"][-1].content == "Invalid Inputs."

def _invoke_agent(message:HumanMessage, context:WorkflowContext) -> dict[str, Any]:
    return supervisor.invoke({"messages": [message]},
                             context=context)
