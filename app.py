import os

import flask
import requests

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['MEETUP_API_KEY'] = os.environ['MEETUP_API_KEY']

API_ROOT = 'https://api.meetup.com/animechicago'

@app.route('/digest')
def digest():
    uri = '{API_ROOT}/events?&sign=true&photo-host=public&page=20&sign=true&key={MEETUP_API_KEY}'.format(
        API_ROOT=API_ROOT,
        MEETUP_API_KEY=app.config['MEETUP_API_KEY'])
    response = requests.get(uri)
    return flask.jsonify(response.json())

@app.route('/newsletter')
def newsletter():
    pass