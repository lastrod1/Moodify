# Add stuff for CRUD functionality
from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from .. import db
from ..models import Genre, Mood, Song, Login, UserLikedSongs
from datetime import datetime

main = Blueprint('main', __name__)

def get_user():
    username = request.headers.get('Authorization')
    if username:
        user = Login.query.filter_by(username=username).first()
        return user
    return None

def get_genres():
    try:
        genres = db.session.execute(
            select(Genre)
        ).scalars().all()

        genre_list = [{"id": genre.genre_id, "name": genre.genre_name} for genre in genres]
        return {'genres': genre_list}
    
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return None
    
def get_moods():
    try:
        moods = db.session.execute(
            select(Mood)
        ).scalars().all()

        mood_list = [{"id": mood.mood_id, "name": mood.mood_name} for mood in moods]
        return {'moods': mood_list}
    
    except Exception as e:
        print(f"Error fetching moods: {e}")
        return None

@main.route('/genres')
def getGenres():
    data = get_genres()
    if data:
        return jsonify(data), 200
    return jsonify({'message': 'Could not fetch data'}), 500

@main.route('/moods')
def getMoods():
    data = get_moods()
    if data:
        return jsonify(data), 200
    return jsonify({'message': 'Could not fetch data'}), 500

@main.route('/load-songs', methods=['GET'])
def loadSongs():
    moods_str = request.args.get('moods', '')
    genres_str = request.args.get('genres', '')

    selected_moods = list(filter(None, moods_str.split(',')))
    selected_genres = list(filter(None, genres_str.split(',')))

    if not selected_moods and not selected_genres:
        return jsonify({"message": "Please select at least one mood or genre filter"}), 400

    try:
        mood_ids = [int(m) for m in selected_moods]
        genre_ids = [int(g) for g in selected_genres]
    except ValueError as e:
        return jsonify({"error": f"Invalid format. Mood and Genre IDs must be numeric. Error: {str(e)}"}), 400

    try:
        mood_condition = Song.mood_id.in_(mood_ids)
        genre_condition = Song.genre_id.in_(genre_ids)

        or_clause = or_(mood_condition, genre_condition)

        statement = select(Song).where(or_clause)

        song_objects = db.session.execute(statement).scalars().all()
        song_list = [
            {
                "song_id": song.song_id,
                "spotify_id": song.spotify_id,
                "title": song.title,
                "artist": song.artist,
                "mood_id": song.mood_id,
                "genre_id": song.genre_id,
                "image_url": song.image_url
            }
            for song in song_objects
        ]
        return jsonify({
            "status": "success",
            "count": len(song_list),
            "songs": song_list,
            "filters_applied": {
                "mood_ids": mood_ids,
                "genre_ids": genre_ids
            }
        })
    except Exception as e:
        print(f"Error fetching songs: {e}")
        return jsonify({"error": f"An error occurred while fetching songs. Error: {str(e)}"}), 500

@main.route('/like', methods=['POST'])
def likeSong():
    current_user = get_user();

    if current_user is None:
        return jsonify({'error': 'Not able to find account'}), 400
    
    username = current_user.username
    song_title = request.get_json().get('song_title')
    dateToStore = datetime.now()

    statement = select(Song.song_id).where(
        Song.title == song_title
    )
    songID = db.session.execute(statement).scalars().first()
    print(song_title)
    if songID is None:
        return jsonify({'error': 'Song not found in database'}), 404

    statement = select(UserLikedSongs).where(
        UserLikedSongs.song_id == songID,
        UserLikedSongs.username == username
    )

    already_liked_song = db.session.execute(statement).scalars().first()

    if(already_liked_song):
        db.session.delete(already_liked_song)
        db.session.commit()
        return jsonify({'message': 'Deleting liked song successful'}), 200
    else:
        new_like = UserLikedSongs(
            username = username,
            song_id = songID,
            date_liked = dateToStore
        )
        db.session.add(new_like)
        db.session.commit()

    return jsonify({'message': 'Adding liked song successful'}), 201

@main.route('/liked-songs', methods=['GET'])
def getLikedSongs():   
    statement = select(UserLikedSongs)
    likedSongs = db.session.scalars(statement).all()
    likedSongsDict = [
        {
            'username': song.username,
            'song_id': song.song_id,
            'date_liked': song.date_liked
        }
        for song in likedSongs
    ]

    return jsonify(likedSongsDict), 200

# this probably isn't the best name for the route but its fine for now
@main.route('/is-liked', methods=['GET'])
def isLiked():
    song_title = request.args.get('song_title')
    username = request.args.get('username')

    statement = select(Song.song_id).where(
        Song.title == song_title
    )
    song_id = db.session.execute(statement).scalars().first()

    if not song_id:
        return jsonify({"error": "Song could not be found in database"}), 400

    statement = select(UserLikedSongs).where(
        UserLikedSongs.song_id == song_id,
        UserLikedSongs.username == username
    )
    liked_song = db.session.execute(statement).scalars().first()

    if not song_id:
        return jsonify({"error": "Song could not be found in database"}), 400
    
    return jsonify({
        "is_liked": liked_song is not None,
        "song_id": song_id
    }), 200