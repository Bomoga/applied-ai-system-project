"""Plain-language explanation generator for TuneMatch recommendations."""


def explain(song: dict, profile: dict) -> str:
    """Generate a human-readable explanation of why a song was recommended.

    Lists which scoring rules fired for the song. Format:
      "[Title] by [Artist] (score: X.X) — Matched: genre, mood, energy"
    If no rules fired:
      "[Title] by [Artist] (score: 0.0) — No strong matches, but included as a suggestion."
    """
    pass
