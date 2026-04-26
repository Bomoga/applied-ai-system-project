"""Plain-language explanation generator for TuneMatch recommendations."""


def explain(song: dict, profile: dict) -> str:
    """Generate a human-readable explanation of why a song was recommended.

    Lists which scoring rules fired for the song. Format:
      "[Title] by [Artist] (score: X.X) — Matched: genre, mood, energy"
    If no rules fired:
      "[Title] by [Artist] (score: 0.0) — No strong matches, but included as a suggestion."
    """
    matched: list[str] = []

    if song["genre"] == profile["genre"]:
        matched.append("genre")

    if song["mood"] == profile["mood"]:
        matched.append("mood")

    energy_diff = abs(float(song["energy"]) - float(profile["energy"]))
    if energy_diff <= 0.25:
        matched.append("energy")

    if profile["likes_acoustic"] and float(song["acousticness"]) >= 0.6:
        matched.append("acoustic")

    if not profile["likes_acoustic"] and float(song["acousticness"]) <= 0.4:
        matched.append("non-acoustic")

    score = song.get("score", 0.0)
    header = f"{song['title']} by {song['artist']} (score: {score:.1f})"

    if not matched:
        return f"{header} — No strong matches, but included as a suggestion."

    return f"{header} — Matched: {', '.join(matched)}"
