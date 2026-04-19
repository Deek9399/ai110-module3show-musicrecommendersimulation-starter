"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs, MAX_SCORE


# ── User profiles ─────────────────────────────────────────────────────────────
PROFILES = {
    "High-Energy Pop": {
        "genre":               "pop",
        "related_genres":      ["indie pop", "synthwave"],
        "mood":                "happy",
        "target_energy":       0.90,
        "target_valence":      0.82,
        "target_acousticness": 0.10,
        "likes_acoustic":      False,
    },
    "Chill Lofi": {
        "genre":               "lofi",
        "related_genres":      ["ambient", "jazz"],
        "mood":                "chill",
        "target_energy":       0.35,
        "target_valence":      0.60,
        "target_acousticness": 0.80,
        "likes_acoustic":      True,
    },
    "Deep Intense Rock": {
        "genre":               "rock",
        "related_genres":      ["synthwave"],
        "mood":                "intense",
        "target_energy":       0.90,
        "target_valence":      0.45,
        "target_acousticness": 0.10,
        "likes_acoustic":      False,
    },
    "Late Night Moody": {
        "genre":               "synthwave",
        "related_genres":      ["indie pop", "rock"],
        "mood":                "moody",
        "target_energy":       0.75,
        "target_valence":      0.48,
        "target_acousticness": 0.18,
        "likes_acoustic":      False,
    },
    "Jazz Coffee Shop": {
        "genre":               "jazz",
        "related_genres":      ["lofi", "ambient"],
        "mood":                "relaxed",
        "target_energy":       0.40,
        "target_valence":      0.72,
        "target_acousticness": 0.87,
        "likes_acoustic":      True,
    },
}


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 3) -> None:
    """Prints a formatted recommendation block for one user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    max_score = MAX_SCORE

    print()
    print("=" * 52)
    print(f"  {label.upper()}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['target_energy']}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled = int((score / max_score) * 20)
        score_bar  = "#" * bar_filled + "-" * (20 - bar_filled)

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       {song['genre']} · {song['mood']} · energy {song['energy']}")
        print(f"       Score : {score:.2f} / {max_score:.1f}  [{score_bar}]")
        print(f"       Why   : {explanation}")

    print()
    print(f"  {len(recommendations)} songs shown from {len(songs)}-song catalog")
    print("=" * 52)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in PROFILES.items():
        print_recommendations(label, prefs, songs, k=3)


if __name__ == "__main__":
    main()
