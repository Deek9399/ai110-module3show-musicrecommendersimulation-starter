"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile — target values for all scored features
    user_prefs = {
        # Categorical preferences (soft filters — related genres get partial credit)
        "genre":          "pop",              # primary genre preference
        "related_genres": ["indie pop", "synthwave"],  # also acceptable genres
        "mood":           "happy",            # preferred mood

        # Continuous preferences (scored with squared distance, range 0.0–1.0)
        "target_energy":       0.80,   # prefers high-energy tracks
        "target_valence":      0.82,   # prefers bright, positive-sounding music
        "target_acousticness": 0.20,   # prefers produced/electronic over acoustic

        # Boolean preference (maps directly to UserProfile dataclass)
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # ── Header ────────────────────────────────────────────────────────────────
    max_score = 6.0
    print()
    print("=" * 52)
    print("  MUSIC RECOMMENDATIONS")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['target_energy']}")
    print("=" * 52)

    # ── Results ───────────────────────────────────────────────────────────────
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled  = int((score / max_score) * 20)
        score_bar   = "#" * bar_filled + "-" * (20 - bar_filled)

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       {song['genre']} · {song['mood']} · energy {song['energy']}")
        print(f"       Score : {score:.2f} / {max_score:.1f}  [{score_bar}]")
        print(f"       Why   : {explanation}")

    # ── Footer ────────────────────────────────────────────────────────────────
    print()
    print("=" * 52)
    print(f"  {len(recommendations)} songs shown from {len(songs)}-song catalog")
    print("=" * 52)
    print()


if __name__ == "__main__":
    main()
