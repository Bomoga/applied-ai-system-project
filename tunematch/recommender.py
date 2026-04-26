"""Ranking and top-k selection for TuneMatch."""

from .scorer import score_song


def recommend(catalog: list[dict], profile: dict, k: int = 5) -> list[dict]:
    """Score every song in catalog and return the top-k matches.

    Attaches a 'score' key to each returned song dict.
    Results are sorted descending by score.
    """
    scored = []
    for song in catalog:
        entry = dict(song)
        entry["score"] = score_song(song, profile)
        scored.append(entry)

    scored.sort(key=lambda s: s["score"], reverse=True)
    return scored[:k]
