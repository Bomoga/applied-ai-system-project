"""Tests for tunematch.guardrails.validate_profile and setup_logging."""

import logging
import os

import pytest

from tunematch.guardrails import validate_profile, setup_logging

VALID_PROFILE = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.7,
    "likes_acoustic": False,
}


def test_valid_profile_passes_through():
    """A fully valid profile is returned unchanged (with energy cast to float)."""
    result = validate_profile(VALID_PROFILE)
    assert result["genre"] == "pop"
    assert result["mood"] == "happy"
    assert result["energy"] == pytest.approx(0.7)
    assert result["likes_acoustic"] is False


def test_missing_genre_raises_value_error():
    """ValueError is raised when 'genre' is absent from the profile."""
    profile = {k: v for k, v in VALID_PROFILE.items() if k != "genre"}
    with pytest.raises(ValueError, match="genre"):
        validate_profile(profile)


def test_missing_mood_raises_value_error():
    """ValueError is raised when 'mood' is absent from the profile."""
    profile = {k: v for k, v in VALID_PROFILE.items() if k != "mood"}
    with pytest.raises(ValueError, match="mood"):
        validate_profile(profile)


def test_missing_energy_raises_value_error():
    """ValueError is raised when 'energy' is absent from the profile."""
    profile = {k: v for k, v in VALID_PROFILE.items() if k != "energy"}
    with pytest.raises(ValueError, match="energy"):
        validate_profile(profile)


def test_missing_likes_acoustic_raises_value_error():
    """ValueError is raised when 'likes_acoustic' is absent from the profile."""
    profile = {k: v for k, v in VALID_PROFILE.items() if k != "likes_acoustic"}
    with pytest.raises(ValueError, match="likes_acoustic"):
        validate_profile(profile)


def test_invalid_genre_raises_value_error():
    """ValueError is raised for a genre not in the allowed set."""
    profile = {**VALID_PROFILE, "genre": "country"}
    with pytest.raises(ValueError, match="genre"):
        validate_profile(profile)


def test_invalid_mood_raises_value_error():
    """ValueError is raised for a mood not in the allowed set."""
    profile = {**VALID_PROFILE, "mood": "relaxed"}
    with pytest.raises(ValueError, match="mood"):
        validate_profile(profile)


def test_energy_above_one_raises_value_error():
    """ValueError is raised when energy is greater than 1.0."""
    profile = {**VALID_PROFILE, "energy": 1.5}
    with pytest.raises(ValueError, match="energy"):
        validate_profile(profile)


def test_energy_below_zero_raises_value_error():
    """ValueError is raised when energy is negative."""
    profile = {**VALID_PROFILE, "energy": -0.1}
    with pytest.raises(ValueError, match="energy"):
        validate_profile(profile)


def test_likes_acoustic_non_bool_raises_type_error():
    """TypeError is raised when likes_acoustic is not a boolean."""
    profile = {**VALID_PROFILE, "likes_acoustic": "yes"}
    with pytest.raises(TypeError):
        validate_profile(profile)


def test_likes_acoustic_integer_raises_type_error():
    """TypeError is raised when likes_acoustic is an integer (0 or 1), not a bool."""
    profile = {**VALID_PROFILE, "likes_acoustic": 1}
    with pytest.raises(TypeError):
        validate_profile(profile)


def test_setup_logging_returns_logger(tmp_path):
    """setup_logging returns a Logger named 'tunematch'."""
    # Reset handlers to avoid pollution between test runs
    logger = logging.getLogger("tunematch")
    logger.handlers.clear()

    result = setup_logging(log_dir=str(tmp_path))
    assert isinstance(result, logging.Logger)
    assert result.name == "tunematch"


def test_setup_logging_creates_log_file(tmp_path):
    """setup_logging creates logs/tunematch.log inside the given log_dir."""
    logger = logging.getLogger("tunematch")
    logger.handlers.clear()

    setup_logging(log_dir=str(tmp_path))
    assert os.path.exists(os.path.join(str(tmp_path), "tunematch.log"))
