# Add stuff for CRUD functionality
from flask import Blueprint, jsonify
from sqlalchemy import select
from .. import db
from ..models import Genre, Mood

main = Blueprint('main', __name__)

def get_genres():
    try:
        genres = db.session.execute(
            select(Genre)
        ).scalars().all()

        genre_list = [genre.genre_name for genre in genres]
        return {'genres': genre_list}
    
    except Exception as e:
        print(f"Error fetching genres: {e}")
        return None
    
def get_moods():
    try:
        moods = db.session.execute(
            select(Mood)
        ).scalars().all()

        mood_list = [mood.mood_name for mood in moods]
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