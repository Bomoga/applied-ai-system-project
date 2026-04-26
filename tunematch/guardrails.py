"""Input validation and logging setup for TuneMatch."""

import logging
import os
import sys

ALLOWED_GENRES = {"pop", "rock", "lofi", "edm", "hiphop", "jazz", "metal", "classical"}
ALLOWED_MOODS = {"happy", "chill", "intense", "sad", "energetic", "romantic"}

REQUIRED_KEYS = {"genre", "mood", "energy", "likes_acoustic"}


def validate_profile(profile: dict) -> dict:
    """Validate a user profile dict and return it if valid.

    Raises ValueError for missing keys, invalid genre/mood, or energy out of [0,1].
    Raises TypeError if likes_acoustic is not a bool.
    """
    missing = REQUIRED_KEYS - set(profile.keys())
    if missing:
        raise ValueError(f"Profile is missing required fields: {sorted(missing)}")

    if profile["genre"] not in ALLOWED_GENRES:
        raise ValueError(
            f"Invalid genre '{profile['genre']}'. Must be one of: {sorted(ALLOWED_GENRES)}"
        )

    if profile["mood"] not in ALLOWED_MOODS:
        raise ValueError(
            f"Invalid mood '{profile['mood']}'. Must be one of: {sorted(ALLOWED_MOODS)}"
        )

    energy = profile["energy"]
    if not isinstance(energy, (int, float)) or not (0.0 <= float(energy) <= 1.0):
        raise ValueError(
            f"Invalid energy '{energy}'. Must be a float in [0.0, 1.0]."
        )

    if not isinstance(profile["likes_acoustic"], bool):
        raise TypeError(
            f"likes_acoustic must be a bool, got {type(profile['likes_acoustic']).__name__}."
        )

    return {**profile, "energy": float(profile["energy"])}


def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Create and configure the tunematch logger.

    Logs to both logs/tunematch.log (append) and stdout. Creates log_dir
    if it does not exist. Returns the configured logger.
    """
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("tunematch")
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(os.path.join(log_dir, "tunematch.log"), mode="a")
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(fmt)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
