"""Weighted rule-based scoring engine for TuneMatch."""


def score_song(song: dict, profile: dict) -> float:
    """Score a single song against a user profile using additive weighted rules.

    Rules:
      genre match          → +3.0
      mood match           → +2.0
      energy within 0.10   → +2.0
      energy within 0.25   → +1.0  (stacks with above)
      acoustic match       → +1.5 or +1.0 depending on preference

    Returns the total score as a float (max 9.5).
    """
    pass
