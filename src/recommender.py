import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # Columns that must be numeric so we can do math on them later.
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip blank trailing rows if present.
            if not row.get("id"):
                continue
            song: Dict = dict(row)
            for field in int_fields:
                song[field] = int(song[field])
            for field in float_fields:
                song[field] = float(song[field])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # Algorithm Recipe (see README):
    #   (2.0 * genre) + (1.0 * mood) + (1.0 * energy_closeness) + (0.5 * acoustic)
    score = 0.0
    reasons: List[str] = []

    # Categorical: genre weighted above mood.
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy: closeness = 1 - |song_energy - target_energy|, on a [0, 1] scale.
    closeness = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    energy_points = 1.0 * closeness
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    # Acousticness: bucket the song by the 0.5 threshold, then compare to preference.
    song_is_acoustic = song["acousticness"] > 0.5
    if song_is_acoustic == user_prefs["likes_acoustic"]:
        score += 0.5
        reasons.append("acoustic match (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # 1. Judge every song in the catalog with score_song.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    # 2. Rank: highest score first, breaking ties alphabetically by title.
    #    We negate the score so it sorts descending while title stays ascending.
    scored.sort(key=lambda item: (-item[1], item[0]["title"]))

    # 3. Return only the top k results.
    return scored[:k]
