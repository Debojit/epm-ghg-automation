from datetime import datetime

from app.agents.analysis import analyser
from app.models.agent import PromptAnalysis

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

def test_valid_input():
    """
    Input: Valid country and year.
    Expected: Correct ISO code and year returned.
    """
    result = analyser.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": "Please find GHG conversion factors for the United Kingdom in 2025"
                }
            ]
        })
    response_msg = result["structured_response"]
    assert isinstance(response_msg, PromptAnalysis)
    assert response_msg.country_code.upper() == "GB"
    assert response_msg.year == "2025"

def test_invalid_country_valid_year():
    """
    Input: Invalid country name, valid year.
    Expected: country_code == 'Invalid'
    """
    result = analyser.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": "Please find GHG conversion factors for Wakanda in 2025"
                }
            ]
        })
    response_msg = result["structured_response"]
    assert response_msg.country_code == "Invalid"
    assert response_msg.year == "2025"

def test_empty_country_valid_year():
    """
    Input: Empty country, valid year.
    Expected: country_code == 'Invalid'
    """
    result = analyser.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": "Please find GHG conversion factors in 2025"
                }
            ]
        })
    response_msg = result["structured_response"]
    assert response_msg.country_code == "Invalid"
    assert response_msg.year == "2025"

def test_valid_country_empty_year():
    """
    Input: Valid country, empty year.
    Expected: year should auto-fill to current or previous year per June rule.
    """
    result = analyser.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": "Please find GHG conversion factors for Japan."
                }
            ]
        })
    response_msg = result["structured_response"]
    assert response_msg.country_code.upper() == "JP"

    # Determine expected auto-year logic
    now = datetime.now()
    expected_year = str(now.year if now.month > 6 else now.year - 1)
    assert response_msg.year == expected_year
