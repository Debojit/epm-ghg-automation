import pytest

from app.agents.analysis import analyser

def test_api_key_works():
    """
    Test that the LLM API key is correctly configured and model can respond.
    """
    try:
        result = analyser.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": "Testing connectivity"
                }
            ]
        })
        assert result["structured_response"] is not None
    except Exception as e:
        pytest.fail(f"LLM invocation failed — check your API key or network: {e}")