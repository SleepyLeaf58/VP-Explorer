from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    games = db.relationship('Game', backref='User')

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    organizer = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    objects = db.relationship('Object', backref='Object')
    

class Object(db.Model):
    __tablename__ = 'object'
    id = db.Column(db.Integer, primary_key=True)
    riddle = db.Column(db.String())
    room = db.Column(db.String(50))
    code = db.Column(db.String(50))
    game_id = user_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    