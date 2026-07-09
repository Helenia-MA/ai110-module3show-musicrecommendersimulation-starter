"""
Command line runner + system evaluation for the Music Recommender Simulation.

This file helps you quickly run and test the recommender, and it contains a
small evaluation harness that probes the scoring logic with a mix of normal
and "adversarial" (edge case) user profiles.

Functions implemented in recommender.py:
- load_songs
- score_song
- recommend_songs

Scoring recipe (see README / score_song):
    (2.0 * genre) + (1.0 * mood) + (1.0 * energy_closeness) + (0.5 * acoustic)
Max possible score = 4.5
"""

from typing import Dict, List

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# 1. Normal profiles — realistic listeners we expect the recommender to serve.
# ---------------------------------------------------------------------------
NORMAL_PROFILES: Dict[str, Dict] = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
}


# ---------------------------------------------------------------------------
# 2. Adversarial / edge case profiles — designed to "trick" the scorer or
#    reveal surprising behavior. Each note explains the hypothesis we're
#    testing.
# ---------------------------------------------------------------------------
ADVERSARIAL_PROFILES: Dict[str, Dict] = {
    # Conflicting signals: wants maximum energy but a sad mood. Almost no song
    # is both, so genre + energy_closeness should dominate and mood rarely hits.
    "Conflicted (energy 0.9 + sad)": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    # Genre that does not exist in the catalog. Tests that the 2.0 genre weight
    # simply never fires and results fall back to energy/mood/acoustic.
    "Nonexistent genre (polka)": {
        "favorite_genre": "polka",
        "favorite_mood": "happy",
        "target_energy": 0.5,
        "likes_acoustic": False,
    },
    # Everything blank/neutral. No genre or mood will ever match; ranking is
    # decided purely by energy closeness (target 0.5) and the acoustic bucket.
    # This exposes how ties are broken (alphabetical by title).
    "Neutral / empty prefs": {
        "favorite_genre": "",
        "favorite_mood": "",
        "target_energy": 0.5,
        "likes_acoustic": False,
    },
    # Genre/mood match but the LOWEST possible energy target vs. a high-energy
    # genre. Tests the tug-of-war between the strong genre weight and a large
    # energy penalty.
    "Rock lover who wants calm (energy 0.0)": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.0,
        "likes_acoustic": True,
    },
}


def run_profile(name: str, user_prefs: Dict, songs: List[Dict], k: int = 5) -> None:
    """Run the recommender for one profile and print its top-k results."""
    print("=" * 70)
    print(f"PROFILE: {name}")
    print(
        "  prefs: "
        f'genre={user_prefs["favorite_genre"]!r}, '
        f'mood={user_prefs["favorite_mood"]!r}, '
        f'target_energy={user_prefs["target_energy"]}, '
        f'likes_acoustic={user_prefs["likes_acoustic"]}'
    )
    print("-" * 70)

    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, (song, score, explanation) in enumerate(recommendations):
        print(
            f"  {i + 1}. {song['title']:<22} "
            f"[{song['genre']}/{song['mood']}, energy={song['energy']}]  "
            f"score={score:.2f}"
        )
        print(f"       reason: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    print("#" * 70)
    print("# NORMAL PROFILES")
    print("#" * 70 + "\n")
    for name, prefs in NORMAL_PROFILES.items():
        run_profile(name, prefs, songs)

    print("#" * 70)
    print("# ADVERSARIAL / EDGE CASE PROFILES")
    print("#" * 70 + "\n")
    for name, prefs in ADVERSARIAL_PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
