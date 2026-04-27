"""Tests for tunematch.recommender.recommend."""

import pytest

from tunematch.recommender import recommend

PROFILE = {"genre": "pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False}


def make_catalog(n: int = 10) -> list[dict]:
    """Build a synthetic catalog of n songs with varying genres and moods."""
    genres = ["pop", "rock", "lofi", "edm", "hiphop", "jazz", "metal", "classical"]
    moods = ["happy", "chill", "intense", "sad", "energetic", "romantic"]
    songs = []
    for i in range(n):
        songs.append({
            "id": i + 1,
            "title": f"Song {i + 1}",
            "artist": f"Artist {i + 1}",
            "genre": genres[i % len(genres)],
            "mood": moods[i % len(moods)],
            "energy": round(0.1 * (i % 10), 1),
            "acousticness": round(0.1 * ((i + 3) % 10), 1),
        })
    return songs


def test_recommend_returns_exactly_k_results():
    """recommend returns exactly k results when the catalog has more than k songs."""
    catalog = make_catalog(20)
    results = recommend(catalog, PROFILE, k=5)
    assert len(results) == 5


def test_recommend_sorted_descending_by_score():
    """Results are ordered from highest to lowest score."""
    catalog = make_catalog(20)
    results = recommend(catalog, PROFILE, k=10)
    scores = [s["score"] for s in results]
    assert scores == sorted(scores, reverse=True)


def test_recommend_attaches_score_key():
    """Every returned song dict contains a 'score' key."""
    catalog = make_catalog(10)
    results = recommend(catalog, PROFILE, k=3)
    for song in results:
        assert "score" in song


def test_recommend_k1_returns_best_match():
    """k=1 returns a list with exactly one song -- the highest scorer."""
    catalog = make_catalog(20)
    top1 = recommend(catalog, PROFILE, k=1)
    all_results = recommend(catalog, PROFILE, k=20)
    assert len(top1) == 1
    assert top1[0]["score"] == all_results[0]["score"]


def test_recommend_does_not_mutate_catalog():
    """recommend does not add 'score' to the original catalog dicts."""
    catalog = make_catalog(5)
    recommend(catalog, PROFILE, k=3)
    for song in catalog:
        assert "score" not in song


def test_recommend_k_larger_than_catalog_returns_all():
    """When k > catalog size, all songs are returned."""
    catalog = make_catalog(3)
    results = recommend(catalog, PROFILE, k=100)
    assert len(results) == 3
