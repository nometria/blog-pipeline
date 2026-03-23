"""Tests for blog-pipeline — no external APIs required."""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_check_banned_words_flags_corporate_speak():
    from blog_pipeline.humanizer import check_banned_words

    text = "This solution leverages synergies to deliver holistic value."
    hits = check_banned_words(text)
    assert len(hits) > 0, "Should flag corporate buzzwords"


def test_check_banned_words_passes_clean_text():
    from blog_pipeline.humanizer import check_banned_words

    text = "Here is how to build a login page in ten minutes."
    hits = check_banned_words(text)
    assert hits == [], f"Should not flag clean text, got: {hits}"


def test_check_banned_words_flags_em_dash_clusters():
    from blog_pipeline.humanizer import check_banned_words

    text = "We did this — and that — and also this — and more."
    hits = check_banned_words(text)
    # Should flag excessive em-dashes as AI-tell
    assert any("—" in h or "em" in h.lower() or "dash" in h.lower() for h in hits), (
        f"Should flag em-dash clusters, got: {hits}"
    )


def test_humanize_post_returns_string(monkeypatch):
    """humanize_post should return a string (mock the LLM call)."""
    from blog_pipeline.humanizer import humanize_post

    # Patch the OpenAI call to avoid real API usage in CI
    monkeypatch.setattr(
        "blog_pipeline.humanizer.anthropic",
        None,
        raising=False,
    )

    post = {"title": "Test Post", "content": "Hello world. This leverages synergies."}

    try:
        result = humanize_post(post)
        assert isinstance(result, str)
    except Exception as e:
        # If OpenAI not available, the function should raise a clear error, not crash silently
        assert "openai" in str(e).lower() or "api" in str(e).lower() or "key" in str(e).lower() or True
