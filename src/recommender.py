import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# ── Scoring weights ────────────────────────────────────────────────────────────
# Baseline (original) values:
#   genre_exact=2.0, genre_related=1.0, mood=1.5, energy=1.5, valence=0.5, acousticness=0.5
#   max_score = 6.0
# Current: sensitivity experiment — energy doubled, genre halved
WEIGHTS = {
    "genre_exact":   1.0,   # baseline: 2.0  (halved)
    "genre_related": 0.5,   # baseline: 1.0  (halved)
    "mood":          1.5,   # baseline: 1.5  (unchanged)
    "energy":        3.0,   # baseline: 1.5  (doubled)
    "valence":       0.5,   # baseline: 0.5  (unchanged)
    "acousticness":  0.5,   # baseline: 0.5  (unchanged)
}

# Maximum achievable score under the current WEIGHTS (used for display/normalization)
MAX_SCORE = (
    WEIGHTS["genre_exact"]
    + WEIGHTS["mood"]
    + WEIGHTS["energy"]
    + WEIGHTS["valence"]
    + WEIGHTS["acousticness"]
)  # = 6.5

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
        """Stores the song catalog for use in recommendation and scoring."""
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Returns a relevance score for song against a UserProfile (max varies with WEIGHTS)."""
        score = 0.0

        if song.genre == user.favorite_genre:
            score += WEIGHTS["genre_exact"]

        if song.mood == user.favorite_mood:
            score += WEIGHTS["mood"]

        score += WEIGHTS["energy"] * (1 - (song.energy - user.target_energy) ** 2)

        # acousticness bonus: reward low-acoustic songs for non-acoustic users
        if not user.likes_acoustic:
            score += WEIGHTS["acousticness"] * (1 - song.acousticness)
        else:
            score += WEIGHTS["acousticness"] * song.acousticness

        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k songs sorted by score descending."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a plain-language explanation of why song was recommended."""
        reasons = []

        if song.genre == user.favorite_genre:
            reasons.append(f"matches your favorite genre '{song.genre}'")

        if song.mood == user.favorite_mood:
            reasons.append(f"matches your preferred mood '{song.mood}'")

        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.10:
            reasons.append(f"energy is very close to your target ({song.energy} vs {user.target_energy})")
        elif energy_diff <= 0.25:
            reasons.append(f"energy is fairly close to your target ({song.energy} vs {user.target_energy})")

        if not reasons:
            reasons.append("partially matches your taste profile")

        return "This song was recommended because it " + " and ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """Parses a CSV at csv_path into a list of song dicts with correctly typed numeric fields."""
    # Resolve path relative to the project root (one level above src/)
    project_root = Path(__file__).parent.parent
    path = project_root / csv_path

    int_fields   = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value) if value.strip() else 0
                elif key in float_fields:
                    song[key] = float(value) if value.strip() else 0.0
                else:
                    song[key] = value
            songs.append(song)
    return songs

def score_song(song: Dict, user_prefs: Dict) -> float:
    """Scores a single song dict against user_prefs using genre, mood, and audio feature rules (max = MAX_SCORE)."""
    score = 0.0

    # Genre rule
    if song["genre"] == user_prefs.get("genre"):
        score += WEIGHTS["genre_exact"]
    elif song["genre"] in user_prefs.get("related_genres", []):
        score += WEIGHTS["genre_related"]

    # Mood rule
    if song["mood"] == user_prefs.get("mood"):
        score += WEIGHTS["mood"]

    # Continuous similarity rules (squared distance)
    score += WEIGHTS["energy"]       * (1 - (song["energy"]       - user_prefs.get("target_energy", 0.5))       ** 2)
    score += WEIGHTS["valence"]      * (1 - (song["valence"]      - user_prefs.get("target_valence", 0.5))      ** 2)
    score += WEIGHTS["acousticness"] * (1 - (song["acousticness"] - user_prefs.get("target_acousticness", 0.5)) ** 2)

    return score


def _build_explanation(song: Dict, user_prefs: Dict) -> str:
    """Builds a plain-language explanation for why song was recommended."""
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        reasons.append(f"matches your favorite genre '{song['genre']}'")
    elif song["genre"] in user_prefs.get("related_genres", []):
        reasons.append(f"'{song['genre']}' is close to your favorite genre")

    if song["mood"] == user_prefs.get("mood"):
        reasons.append(f"matches your preferred mood '{song['mood']}'")

    energy_diff = abs(song["energy"] - user_prefs.get("target_energy", 0.5))
    if energy_diff <= 0.10:
        reasons.append(f"energy is very close to your target ({song['energy']} vs {user_prefs.get('target_energy')})")
    elif energy_diff <= 0.25:
        reasons.append(f"energy is fairly close to your target ({song['energy']} vs {user_prefs.get('target_energy')})")

    if not reasons:
        reasons.append("partially matches your taste profile")

    return "Because it " + " and ".join(reasons) + "."


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top-k (song, score, explanation) tuples from songs, ranked by score descending."""
    return sorted(
        (
            (song, score_song(song, user_prefs), _build_explanation(song, user_prefs))
            for song in songs
        ),
        key=lambda x: x[1],
        reverse=True,
    )[:k]
