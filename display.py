from flask import Flask
from flask import request, render_template
from flask import url_for
from flask import redirect
from flask import session
from flask.ext.sqlalchemy import SQLAlchemy

from models import Tweet, db

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def show_entries():
    tweets = Tweet.query.all()
    return render_template('list_tweets.html', tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)
