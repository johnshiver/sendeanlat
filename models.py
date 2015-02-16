import sqlite3 as lite

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://///Users/johnshiver/projects/sendeanlat/sendeanlat/tweets.db"

db = SQLAlchemy(app)


class Tweet(db.Model):
    __tablename__ = "Tweets"
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(100))
    tweet = db.Column(db.String(240))
    hash_tag = db.Column(db.String(240))
    match_term = db.Column(db.String(240))
    time = db.Column(db.DateTime)


def create_table():
    con = lite.connect('tweets.db')
    db.create_all()