"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile (keys match score_song's Algorithm Recipe).
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }
    # User profile: genre=indie, mood=chill, energy=low
    print(f'User profile: genre={user_prefs["favorite_genre"]}, mood={user_prefs["favorite_mood"]}, energy={user_prefs["target_energy"]}, likes_acoustic={user_prefs["likes_acoustic"]}')

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for i, rec in enumerate(recommendations):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{i + 1}. {song['title']} - Score: {score:.2f}")
        print(f"Reason: {explanation}")
        print()


if __name__ == "__main__":
    main()
