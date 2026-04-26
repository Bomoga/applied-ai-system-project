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
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Catalog CSV is missing required columns: {sorted(missing)}")

    df["energy"] = df["energy"].astype(float)
    df["acousticness"] = df["acousticness"].astype(float)

    for col in ("energy", "acousticness"):
        out_of_range = df[(df[col] < 0.0) | (df[col] > 1.0)]
        if not out_of_range.empty:
            logger.warning(
                "Clamping %d out-of-range value(s) in column '%s' to [0.0, 1.0]",
                len(out_of_range),
                col,
            )
        df[col] = df[col].clip(0.0, 1.0)

    return df.to_dict(orient="records")
