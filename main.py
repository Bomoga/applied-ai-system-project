"""TuneMatch — CLI entry point."""

import argparse
import sys

from tunematch import load_catalog, recommend, explain, validate_profile
from tunematch.guardrails import setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="tunematch",
        description="TuneMatch — content-based music recommender",
    )
    parser.add_argument("--genre", required=True, help="Preferred genre (e.g. pop, rock, lofi)")
    parser.add_argument("--mood", required=True, help="Target mood (e.g. happy, chill, intense)")
    parser.add_argument("--energy", required=True, type=float, help="Target energy level (0.0–1.0)")
    parser.add_argument("--acoustic", action="store_true", help="Prefer acoustic tracks")
    parser.add_argument("--top", type=int, default=5, help="Number of recommendations (default: 5)")
    parser.add_argument(
        "--catalog", default="data/songs.csv", help="Path to catalog CSV (default: data/songs.csv)"
    )
    return parser.parse_args()


def main() -> None:
    logger = setup_logging()
    args = parse_args()

    profile = {
        "genre": args.genre,
        "mood": args.mood,
        "energy": args.energy,
        "likes_acoustic": args.acoustic,
    }

    try:
        profile = validate_profile(profile)
    except (ValueError, TypeError) as exc:
        logger.error("Invalid profile: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        catalog = load_catalog(args.catalog)
    except (ValueError, FileNotFoundError, Exception) as exc:
        logger.error("Failed to load catalog: %s", exc)
        print(f"Error loading catalog: {exc}", file=sys.stderr)
        sys.exit(1)

    results = recommend(catalog, profile, k=args.top)

    print(f"\nTuneMatch -- Top {args.top} Recommendations")
    print("-" * 42)
    for i, song in enumerate(results, start=1):
        print(f"{i}. {explain(song, profile)}")

    logger.info("Recommended %d songs for profile: %s", len(results), profile)


if __name__ == "__main__":
    main()
