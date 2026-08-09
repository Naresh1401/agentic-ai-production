"""Unit tests for the eval scorers."""
from scorers import contains_match, llm_judge, matches_schema, refuses, score_case


def test_contains_match():
    assert contains_match("The capital is Paris.", "paris")
    assert not contains_match("London", "paris")


def test_refuses():
    assert refuses("Sorry, I can't do that")
    assert not refuses("Sure, here you go")


def test_matches_schema():
    assert matches_schema('{"a": 1, "b": "x"}', {"a": "int", "b": "str"})
    assert not matches_schema('{"a": "no"}', {"a": "int"})
    assert not matches_schema("not json", {"a": "int"})


def test_score_case():
    assert score_case("Sorry, I cannot", "REFUSE")
    assert score_case("The answer is 144", "144")
    assert not score_case("The answer is 143", "144")


def test_llm_judge_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    score = llm_judge("paris is the capital", "capital of france", "paris capital")
    assert 0.0 <= score <= 1.0
