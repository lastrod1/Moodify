from . import db
from datetime import datetime

# File for defining tables
# Run "flask db init"
# Then "flask db migrate"
# Then "flask db upgrade"
# These will create the table

class UserLikedSongs(db.Model):
    __tablename__ = 'user_liked_songs'

    username = db.Column(db.String(64), db.ForeignKey('login.username'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'), primary_key=True)
    date_liked = db.Column(db.DateTime, default=datetime.utcnow)

class Login(db.Model):
    __tablename__ = 'login'

    username = db.Column(db.String(64), primary_key=True, unique=True)
    password = db.Column(db.String(64), nullable=False)

    liked_songs_links = db.relationship('UserLikedSongs', backref='user', lazy='dynamic')

class Mood(db.Model):
    __tablename__ = 'mood'

    mood_id = db.Column(db.Integer, primary_key=True)
    mood_name = db.Column(db.String(128), nullable=False, unique=True)

    songs = db.relationship('Song', backref='song_type', lazy='dynamic')

class Genre(db.Model):
    __tablename__ = 'genre'

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(128), nullable=False, unique=True)

    songs = db.relationship('Song', backref='genre_type', lazy='dynamic')

class Song(db.Model):
    __tablename__ = 'song'

    song_id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)

    mood_id = db.Column(db.Integer, db.ForeignKey('mood.mood_id'), nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=True)

    liked_by_users = db.relationship('UserLikedSongs', backref='song', lazy='dynamic')
    