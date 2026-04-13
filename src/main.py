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
    print(f"Loaded songs: {len(songs)}.")

    # Starter example profile
    user_prefs = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.8,
    "target_acousticness": 0.2
}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for idx, rec in enumerate(recommendations, 1):
        song = rec['song']
        score = rec['score']
        reasons = rec['reasons']
        
        # Print rank, title, artist, and score
        print(f"#{idx} {song['title']} — {song['artist']}  (score: {score} / 5.0)")
        
        # Print each reason indented with a bullet
        for reason in reasons:
            print(f"   • {reason}")
        
        # Divider line between songs
        print("----------------------------------------")


if __name__ == "__main__":
    main()
