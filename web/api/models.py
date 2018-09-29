from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey

from .app import app

import dateutil.parser

db = SQLAlchemy(app)
db.init_app(app)

class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    def __init__(self, name):
        self.name = name

class Performer(db.Model): 
    __tablename__ = 'performers'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    def __init__(self, name):
        self.name = name

class Song(db.Model):
    __tablename__ = 'songs'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    performer_id = db.Column(db.Integer, ForeignKey('performers.id'), nullable=False)
    performer = db.relationship("Performer", lazy="joined")
    def __init__(self, title, performer):
        self.title = title
        self.performer_id = performer.id

class Play(db.Model):
    __tablename__ = 'plays'
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, ForeignKey('songs.id'), nullable=False)
    channel_id =  db.Column(db.Integer, ForeignKey('channels.id'), nullable=False)
    performer_id = db.Column(db.Integer, ForeignKey('performers.id'), nullable=False)
    start = db.Column(db.DateTime, unique=False, nullable=False)
    end = db.Column(db.DateTime, unique=False, nullable=False)
    channel = db.relationship("Channel", lazy="joined")
    performer = db.relationship("Performer", lazy="joined")
    song = db.relationship("Song", lazy="joined")
    def __init__(self, song, channel, performer, start, end):
        self.song_id = song.id
        self.channel_id = channel.id
        self.performer_id = performer.id
        self.start = dateutil.parser.parse(start)
        self.end = dateutil.parser.parse(end)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)