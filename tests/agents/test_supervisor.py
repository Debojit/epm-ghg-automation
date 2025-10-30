from app.agents.supervisor import supervisor

def test_valid_input():
    """
    Test if the agent workflow is performing normally with valid inputs.

    Inputs: Country Code: GB, Year: 2025
    Expected: Conversion factors download link.
    """
    result = supervisor.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": "Please find GHG conversion factors for the United Kingdom in 2025"
                }
            ]
        })
    import pprint
    pprint.pp(result["messages"][-1].content)
    assert result["messages"][-1] not in (None, "")