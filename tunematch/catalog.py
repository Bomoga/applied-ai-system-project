"""Loads and validates the song catalog from a CSV file."""

import logging
import pandas as pd

logger = logging.getLogger("tunematch")

REQUIRED_COLUMNS = {"id", "title", "artist", "genre", "mood", "energy", "acousticness"}


def load_catalog(path: str) -> list[dict]:
    """Load a song catalog CSV and return a list of song dicts.

    Validates required columns are present and clamps energy/acousticness
    to [0.0, 1.0], logging a warning for any out-of-range values.
    """
    pass
