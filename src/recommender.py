from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
    """Loads songs from a CSV file and returns a list of song dictionaries with parsed numeric fields."""

    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = int(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Takes user preferences and a song, returns a score and list of scoring reasons."""

    score = 0.0
    reasons = []
    
    # Genre match: +2.0
    if song['genre'] == user_prefs.get('favorite_genre'):
        score += 2.0
        reasons.append('genre match (+2.0)')
    
    # Mood match: +1.5
    if song['mood'] == user_prefs.get('favorite_mood'):
        score += 1.5
        reasons.append('mood match (+1.5)')
    
    # Energy proximity: +1.0 × (1 − |song['energy'] − user_prefs['target_energy']|)
    target_energy = max(0.0, min(1.0, user_prefs.get('target_energy', 0.5)))
    energy_proximity = 1.0 * (1 - abs(song['energy'] - target_energy))
    energy_proximity_rounded = round(energy_proximity, 2)
    score += energy_proximity_rounded
    reasons.append(f'energy proximity (+{energy_proximity_rounded})')
    
    # Acousticness proximity: +0.5 × (1 − |song['acousticness'] − user_prefs['target_acousticness']|)
    target_acousticness = max(0.0, min(1.0, user_prefs.get('target_acousticness', 0.5)))
    acousticness_proximity = 0.5 * (1 - abs(song['acousticness'] - target_acousticness))
    acousticness_proximity_rounded = round(acousticness_proximity, 2)
    score += acousticness_proximity_rounded
    reasons.append(f'acousticness proximity (+{acousticness_proximity_rounded})')
    
    return (round(score, 2), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top k songs scored and ranked by user preference compatibility."""
    
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append({
            'song': song,
            'score': score,
            'reasons': reasons
        })
    
    # Use sorted() instead of .sort() because:
    # 1. sorted() returns a new list (immutable approach, safer)
    # 2. sorted() is more functional and chainable
    # 3. .sort() modifies in-place and returns None (harder to use)
    # 4. sorted() is preferred in functional programming paradigms
    top_k = sorted(scored_songs, key=lambda x: x['score'], reverse=True)[:k]
    
    return top_k
