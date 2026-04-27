"""Tests for tunematch.scorer.score_song."""

import pytest

from tunematch.scorer import score_song

BASE_SONG = {
    "genre": "rock",
    "mood": "intense",
    "energy": 0.5,
    "acousticness": 0.2,
}

BASE_PROFILE = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.5,
    "likes_acoustic": False,
}


def test_genre_match_adds_three_points():
    """A matching genre awards +3.0 on top of other applicable rules."""
    song = {**BASE_SONG, "genre": "pop"}
    profile = {**BASE_PROFILE}
    score = score_song(song, profile)
    # genre +3, energy diff=0 fires both energy rules (+2+1), non-acoustic (+1) = 7.0
    assert score == pytest.approx(7.0)


def test_genre_match_isolated():
    """Genre-only match (no other rules fire) gives exactly +3.0."""
    song = {"genre": "pop", "mood": "chill", "energy": 0.0, "acousticness": 0.5}
    profile = {"genre": "pop", "mood": "happy", "energy": 1.0, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(3.0)


def test_mood_match_isolated():
    """Mood-only match gives exactly +2.0."""
    song = {"genre": "rock", "mood": "happy", "energy": 0.0, "acousticness": 0.5}
    profile = {"genre": "pop", "mood": "happy", "energy": 1.0, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(2.0)


def test_energy_within_0_1_adds_two_plus_one():
    """Energy diff <= 0.1 fires both energy rules for +3.0 total from energy."""
    song = {"genre": "rock", "mood": "chill", "energy": 0.55, "acousticness": 0.5}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(3.0)  # +2 (within 0.1) + +1 (within 0.25)


def test_energy_within_0_25_adds_one_only():
    """Energy diff in (0.1, 0.25] fires only the second energy rule for +1.0."""
    song = {"genre": "rock", "mood": "chill", "energy": 0.7, "acousticness": 0.5}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(1.0)


def test_energy_beyond_0_25_adds_nothing():
    """Energy diff > 0.25 earns 0 points from energy rules."""
    song = {"genre": "rock", "mood": "chill", "energy": 0.9, "acousticness": 0.5}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(0.0)


def test_acoustic_bonus_when_likes_acoustic_and_high_acousticness():
    """likes_acoustic=True with acousticness >= 0.6 awards +1.5."""
    song = {"genre": "rock", "mood": "chill", "energy": 0.9, "acousticness": 0.7}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": True}
    score = score_song(song, profile)
    assert score == pytest.approx(1.5)


def test_acoustic_bonus_not_awarded_when_acousticness_too_low():
    """likes_acoustic=True with acousticness < 0.6 does not award acoustic bonus."""
    song = {"genre": "rock", "mood": "chill", "energy": 0.9, "acousticness": 0.5}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": True}
    score = score_song(song, profile)
    assert score == pytest.approx(0.0)


def test_non_acoustic_bonus_when_not_acoustic_and_low_acousticness():
    """likes_acoustic=False with acousticness <= 0.4 awards +1.0."""
    song = {"genre": "rock", "mood": "chill", "energy": 0.9, "acousticness": 0.3}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(1.0)


def test_non_acoustic_bonus_not_awarded_when_acousticness_too_high():
    """likes_acoustic=False with acousticness > 0.4 does not award non-acoustic bonus."""
    song = {"genre": "rock", "mood": "chill", "energy": 0.9, "acousticness": 0.6}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(0.0)


def test_all_rules_match_reaches_maximum():
    """A song matching every rule earns the maximum score of 9.5."""
    song = {"genre": "pop", "mood": "happy", "energy": 0.5, "acousticness": 0.7}
    profile = {"genre": "pop", "mood": "happy", "energy": 0.5, "likes_acoustic": True}
    score = score_song(song, profile)
    assert score == pytest.approx(9.5)


def test_no_rules_match_scores_zero():
    """A song matching no rules scores exactly 0.0."""
    song = {"genre": "metal", "mood": "intense", "energy": 0.0, "acousticness": 0.5}
    profile = {"genre": "pop", "mood": "happy", "energy": 1.0, "likes_acoustic": False}
    score = score_song(song, profile)
    assert score == pytest.approx(0.0)
