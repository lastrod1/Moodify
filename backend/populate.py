import sys
import os
from flask.cli import with_appcontext

# Add the parent directory (backend folder) to the system path.
# This ensures that Python can correctly import the 'moodify_api' package 
# when this script is run directly from the project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import necessary components from your Flask application package
from moodify_api import create_app, db
from moodify_api.models import Mood, Genre, Song

# --- Initial Data (Matching UI and previous DB state) ---
INITIAL_GENRES = [
    "Pop", "Hip Hop", "R&B", "Rock", "Electronic/Dance", "Latin Pop", 
    "K-Pop", "Indie Folk", "Christian Hip Hop", "Jazz"
]

INITIAL_MOODS = [
    "Euphoric", "Cheerful", "Calm", "Relaxed", "Melancholy", "Somber", 
    "Aggressive", "Pumped", "Neutral", "Driving"
]

# 10 songs based on the data provided, now only using the required columns.
INITIAL_SONGS = [
    {
        # Mood ID 2 (Cheerful), Genre ID 1 (Pop)
        "title": "Shape of You", 
        "artist": "Ed Sheeran", 
        "spotify_id": "7qiZfU4dY1lWllzX7mPBI3", 
        "mood_name": "Cheerful",
        "genre_name": "Pop",
        "image_url": "https://i.scdn.co/image/ab67616d00004851ba5db46f4b838ef6027e6f96"
    },
    {
        # Mood ID 9 (Neutral), Genre ID 2 (Hip Hop)
        "title": "God's Plan", 
        "artist": "Drake", 
        "spotify_id": "6DCZcSspjsKoFjzjrWoCdn", 
        "mood_name": "Neutral",
        "genre_name": "Hip Hop",
        "image_url": "https://i.scdn.co/image/ab67616d0000b273f907de96b9a4fbc04accc0d5"
    },
    {
        # Mood ID 4 (Relaxed), Genre ID 3 (R&B)
        "title": "Killing Me Softly With His Song", 
        "artist": "The Fugees", 
        "spotify_id": "0Q0IVlqMV64kNLlwjPj0Hl", 
        "mood_name": "Relaxed",
        "genre_name": "R&B",
        "image_url": "https://i.scdn.co/image/ab67616d0000b2735b7865be7f7fcc05faec6137"
    },
    {
        # Mood ID 8 (Pumped), Genre ID 4 (Rock)
        "title": "Smells Like Teen Spirit", 
        "artist": "Nirvana", 
        "spotify_id": "5ghIJDpPoe3CfHMGu71E6T", 
        "mood_name": "Pumped",
        "genre_name": "Rock",
        "image_url": "https://i.scdn.co/image/ab67616d00001e02e175a19e530c898d167d39bf"
    },
    {
        # Mood ID 7 (Aggressive), Genre ID 5 (Electronic/Dance)
        "title": "Levels", 
        "artist": "Avicii", 
        "spotify_id": "6Xe9wT5xeZETPwtaP2ynUz", 
        "mood_name": "Aggressive",
        "genre_name": "Electronic/Dance",
        "image_url": "https://i.scdn.co/image/ab67616d00001e02ffb343926530168be4724dd4"
    },
    {
        # Mood ID 10 (Driving), Genre ID 6 (Latin Pop)
        "title": "Despacito", 
        "artist": "Luis Fonsi", 
        "spotify_id": "6habFhsOp2NvshLv26DqMb", 
        "mood_name": "Driving",
        "genre_name": "Latin Pop",
        "image_url": "https://i.scdn.co/image/ab67616d00004851ef0d4234e1a645740f77d59c"
    },
    {
        # Mood ID 1 (Euphoric), Genre ID 7 (K-Pop)
        "title": "Dynamite", 
        "artist": "BTS", 
        "spotify_id": "5QDLhrAOJJdNAmCTJ8xMyW", 
        "mood_name": "Euphoric",
        "genre_name": "K-Pop",
        "image_url": "https://i.scdn.co/image/ab67616d0000b273c07d5d2fdc02ae252fcd07e5"
    },
    {
        # Mood ID 3 (Calm), Genre ID 8 (Indie Folk)
        "title": "Ophelia", 
        "artist": "The Lumineers", 
        "spotify_id": "14AyWf6y7KlWWLfAjdKMKI", 
        "mood_name": "Calm",
        "genre_name": "Indie Folk",
        "image_url": "https://i.scdn.co/image/ab67616d0000485121b550b66cf1391c6642088c"
    },
    {
        # Mood ID 6 (Somber), Genre ID 9 (Christian Hip Hop)
        "title": "The Vultures", 
        "artist": "Lecrae", 
        "spotify_id": "1Vc1zkJP3bmNXCJncvXDYN", 
        "mood_name": "Somber",
        "genre_name": "Christian Hip Hop",
        "image_url": "https://i.scdn.co/image/ab67616d00004851beb851741290255b89e7c16d"
    },
    {
        # Mood ID 5 (Melancholy), Genre ID 10 (Jazz)
        "title": "Blue in Green", 
        "artist": "Miles Davis", 
        "spotify_id": "1zNXFzNXEsSENUgr", 
        "mood_name": "Melancholy",
        "genre_name": "Jazz",
        "image_url": "https://i.scdn.co/image/ab67616d0000b27353916cd700eef7318d795479"
    }
]

# --- Population Logic ---

def populate_initial_data(app):
    """
    Handles the core logic for checking if data exists and adding it.
    """
    with app.app_context():
        print("--- Starting database population ---")

        # 1. Populate Genres (checking for existence first)
        existing_genres = {g.genre_name for g in db.session.execute(db.select(Genre.genre_name)).scalars().all()}
        for name in INITIAL_GENRES:
            if name not in existing_genres:
                db.session.add(Genre(genre_name=name))
                print(f"Added Genre: {name}")
        
        # 2. Populate Moods (checking for existence first)
        existing_moods = {m.mood_name for m in db.session.execute(db.select(Mood.mood_name)).scalars().all()}
        for name in INITIAL_MOODS:
            if name not in existing_moods:
                db.session.add(Mood(mood_name=name))
                print(f"Added Mood: {name}")

        # Commit Moods and Genres first to ensure they have IDs assigned
        try:
            db.session.commit()
            print("Genres and Moods committed successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing Genres/Moods: {e}")
            return # Stop if the initial commit fails

        # Re-fetch the newly created data for use in the Song foreign keys
        genre_map = {g.genre_name: g.genre_id for g in Genre.query.all()}
        mood_map = {m.mood_name: m.mood_id for m in Mood.query.all()}
        existing_spotify_ids = {s.spotify_id for s in Song.query.all()}


        # 3. Populate Songs (checking for existence by spotify_id)
        for song_data in INITIAL_SONGS:
            if song_data["spotify_id"] not in existing_spotify_ids:
                
                # Check if we have valid IDs for mood and genre before adding the song
                mood_id = mood_map.get(song_data["mood_name"])
                genre_id = genre_map.get(song_data["genre_name"])
                
                if mood_id is None:
                    print(f"ERROR: Could not find Mood ID for '{song_data['mood_name']}'. Skipping song: {song_data['title']}")
                    continue
                if genre_id is None:
                    print(f"ERROR: Could not find Genre ID for '{song_data['genre_name']}'. Skipping song: {song_data['title']}")
                    continue

                new_song = Song(
                    title=song_data["title"],
                    artist=song_data["artist"],
                    spotify_id=song_data["spotify_id"],
                    image_url=song_data["image_url"],
                    mood_id=mood_id,
                    genre_id=genre_id
                )
                db.session.add(new_song)
                print(f"Added Song: {song_data['title']} by {song_data['artist']} (Mood: {song_data['mood_name']}, Genre: {song_data['genre_name']})")

        try:
            db.session.commit()
            print("Initial songs committed successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error committing Songs: {e}")


        print("--- Database population complete ---")

# --- Execution Entry Point ---

if __name__ == '__main__':
    # Initialize the Flask app using the factory function
    app = create_app()
    
    # Run the population script within the application context
    with app.app_context():
        populate_initial_data(app)