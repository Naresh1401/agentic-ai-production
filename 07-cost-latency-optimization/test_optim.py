"""Unit tests for the cost/latency helpers."""
from cache import ExactCache, SemanticCache
from optimize import cost, percentile
from router import Router


def test_exact_cache_hit_miss():
    c = ExactCache()
    assert c.get("q") is None
    c.set("q", "a")
    assert c.get("q") == "a"


def test_semantic_cache_near_duplicate():
    c = SemanticCache(threshold=0.8)
    c.set("What is the capital of France?", "Paris")
    assert c.get("what's the capital of France?") == "Paris"


def test_router_escalates_hard_prompts():
    r = Router()
    assert r.choose("hi") == r.small_model
    assert r.choose("Design a scalable architecture for a platform") == r.large_model
    assert 0.0 <= r.escalation_rate <= 1.0


def test_cost_and_percentile():
    assert cost("small", 1000, 1000) > 0
    assert percentile([1, 2, 3, 4], 50) == 3
