"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs


PROFILES = [
    {
        "name": "Pop / Happy",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    },
    {
        "name": "High-Energy Rock",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    },
    {
        "name": "Chill Lofi",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    },
]


def print_recommendations(profile_name: str, recommendations: list) -> None:
    """Print the top recommendations for a user profile in a readable format."""
    width = 60
    print("\n" + "=" * width)
    print(f"  Profile: {profile_name}")
    print("=" * width)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.")

    for profile in PROFILES:
        recs = recommend_songs(profile["prefs"], songs, k=5)
        print_recommendations(profile["name"], recs)


if __name__ == "__main__":
    main()
