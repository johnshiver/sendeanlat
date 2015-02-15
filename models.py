from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://js231813@localhost/tweet_offerup"

db = SQLAlchemy(app)


class Tweet(db.Model):
    __tablename__ = "offerup_tweets"
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(100))
    text = db.Column(db.String(240))
    timestamp = db.Column(db.DateTime)
