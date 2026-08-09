"""Module 8 concern: retrieval (RAG) over a small support knowledge base.

Uses token-overlap (Jaccard) similarity as a stand-in for embeddings so it runs
with no dependencies. Swap for a real vector store in production.
"""
from __future__ import annotations

KNOWLEDGE_BASE = {
    "refund": "Refunds are processed within 5 business days to the original payment method.",
    "shipping": "Standard shipping takes 3-5 business days; express takes 1-2 days.",
    "hours": "Support is available 9am-5pm on weekdays, excluding public holidays.",
    "password": "Reset your password from the login page via 'Forgot password'.",
    "cancel": "You can cancel a subscription anytime from Account > Billing.",
}


# Common words to ignore so retrieval matches on meaningful terms only.
STOPWORDS = {
    "the", "what", "your", "you", "from", "via", "for", "and", "are", "how",
    "does", "can", "with", "this", "that", "have", "will", "would", "should",
    "long", "much", "many", "when", "where", "which", "there", "their",
}


def _tokens(text: str) -> set[str]:
    return {t for t in text.lower().replace("?", " ").split() if len(t) > 2 and t not in STOPWORDS}


def retrieve(query: str, threshold: float = 0.05) -> tuple[str, float]:
    """Return (best_document, score). Score 0 means nothing relevant found."""
    q = _tokens(query)
    best_text, best_score = "", 0.0
    for key, text in KNOWLEDGE_BASE.items():
        doc = _tokens(f"{key} {text}")
        union = q | doc
        score = len(q & doc) / len(union) if union else 0.0
        if score > best_score:
            best_text, best_score = text, score
    if best_score < threshold:
        return "", 0.0
    return best_text, best_score
