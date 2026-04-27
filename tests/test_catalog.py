"""Tests for tunematch.catalog.load_catalog."""

import pandas as pd
import pytest

from tunematch.catalog import load_catalog


def test_load_catalog_returns_list_of_dicts():
    """load_catalog on the real songs.csv returns a non-empty list of dicts with all required keys."""
    catalog = load_catalog("data/songs.csv")
    assert isinstance(catalog, list)
    assert len(catalog) > 0
    required = {"id", "title", "artist", "genre", "mood", "energy", "acousticness"}
    for song in catalog:
        assert required.issubset(song.keys())


def test_load_catalog_energy_and_acousticness_are_floats():
    """energy and acousticness values in the loaded catalog are Python floats."""
    catalog = load_catalog("data/songs.csv")
    for song in catalog:
        assert isinstance(song["energy"], float)
        assert isinstance(song["acousticness"], float)


def test_load_catalog_raises_on_missing_column(tmp_path):
    """load_catalog raises ValueError when a required column is absent."""
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("id,title,artist,genre,mood,energy\n1,Song,Artist,pop,happy,0.5\n")
    with pytest.raises(ValueError, match="acousticness"):
        load_catalog(str(bad_csv))


def test_load_catalog_raises_listing_all_missing_columns(tmp_path):
    """ValueError message lists every missing column, not just the first."""
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("id,title\n1,Song\n")
    with pytest.raises(ValueError):
        load_catalog(str(bad_csv))


def test_load_catalog_clamps_energy_above_one(tmp_path):
    """energy values above 1.0 are clamped to 1.0 without raising."""
    csv = tmp_path / "songs.csv"
    csv.write_text(
        "id,title,artist,genre,mood,energy,acousticness\n"
        "1,Song,Artist,pop,happy,1.5,0.5\n"
    )
    catalog = load_catalog(str(csv))
    assert catalog[0]["energy"] == 1.0


def test_load_catalog_clamps_energy_below_zero(tmp_path):
    """energy values below 0.0 are clamped to 0.0 without raising."""
    csv = tmp_path / "songs.csv"
    csv.write_text(
        "id,title,artist,genre,mood,energy,acousticness\n"
        "1,Song,Artist,pop,happy,-0.2,0.5\n"
    )
    catalog = load_catalog(str(csv))
    assert catalog[0]["energy"] == 0.0


def test_load_catalog_clamps_acousticness(tmp_path):
    """acousticness values outside [0,1] are clamped silently."""
    csv = tmp_path / "songs.csv"
    csv.write_text(
        "id,title,artist,genre,mood,energy,acousticness\n"
        "1,Song,Artist,pop,happy,0.5,2.0\n"
    )
    catalog = load_catalog(str(csv))
    assert catalog[0]["acousticness"] == 1.0
