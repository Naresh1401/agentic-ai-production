"""Unit tests for the minimal agent loop."""
from agent_demo import calculator, plan, retrieve, run_agent


def test_calculator():
    assert calculator("12 * (3 + 4)") == "84"
    assert calculator("import os") == "unsupported expression"


def test_retrieve():
    assert "5 business days" in retrieve("what is the refund policy?")
    assert retrieve("weather today") == "no relevant document found"


def test_plan_routes_correctly():
    assert plan("what is 2 + 2?")[0] == "calculator"
    assert plan("refund policy")[0] == "retrieve"
    assert plan("say hi")[0] == "answer"


def test_run_agent_uses_tool():
    assert run_agent("What is 6 * 7?") == "42"
