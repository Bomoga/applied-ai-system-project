"""Weighted rule-based scoring engine for TuneMatch."""


def score_song(song: dict, profile: dict) -> float:
    """Score a single song against a user profile using additive weighted rules.

    Rules:
      genre match          → +3.0
      mood match           → +2.0
      energy within 0.10   → +2.0
      energy within 0.25   → +1.0  (stacks with the 0.10 rule)
      acoustic match       → +1.5 or +1.0 depending on preference

    Returns the total score as a float (max 9.5).
    """
    score = 0.0

    if song["genre"] == profile["genre"]:
        score += 3.0

    if song["mood"] == profile["mood"]:
        score += 2.0

    energy_diff = abs(float(song["energy"]) - float(profile["energy"]))
    if energy_diff <= 0.1:
        score += 2.0
    if energy_diff <= 0.25:
        score += 1.0

    if profile["likes_acoustic"] and float(song["acousticness"]) >= 0.6:
        score += 1.5

    if not profile["likes_acoustic"] and float(song["acousticness"]) <= 0.4:
        score += 1.0

    return score
