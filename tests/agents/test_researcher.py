import pytest

from app.agents.research import researcher
from app.models.agent import PromptAnalysis


def test_valid_input():
    """
    Test that the researcher is working normally.
    """
    result = researcher.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": PromptAnalysis(
                        CountryCode="UK", Year="2025"
                    ).model_dump_json(),
                }
            ]
        }
    )
    assert result["messages"][-1].content not in (None, "")


def test_invalid_input():
    """
    Test that the researcher is working normally.
    """
    result = researcher.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": PromptAnalysis(
                        CountryCode="ABC", Year="2025"
                    ).model_dump_json(),
                }
            ]
        }
    )
    assert result["messages"][-1].content == ""
