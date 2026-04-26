"""Input validation and logging setup for TuneMatch."""

import logging
import os

ALLOWED_GENRES = {"pop", "rock", "lofi", "edm", "hiphop", "jazz", "metal", "classical"}
ALLOWED_MOODS = {"happy", "chill", "intense", "sad", "energetic", "romantic"}

REQUIRED_KEYS = {"genre", "mood", "energy", "likes_acoustic"}


def validate_profile(profile: dict) -> dict:
    """Validate a user profile dict and return it if valid.

    Raises ValueError for missing keys, invalid genre/mood, or energy out of [0,1].
    Raises TypeError if likes_acoustic is not a bool.
    """
    pass


def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Create and configure the tunematch logger.

    Logs to both logs/tunematch.log (append) and stdout. Creates log_dir
    if it does not exist. Returns the configured logger.
    """
    pass
