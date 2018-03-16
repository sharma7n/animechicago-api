import os

import flask
import flask_cors
import pendulum
import requests

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['MEETUP_API_KEY'] = os.environ['MEETUP_API_KEY']
flask_cors.CORS(app)

API_ROOT = 'https://api.meetup.com/animechicago'

def meetup_date(meetup):
    return pendulum.from_format(meetup['local_date'], '%Y-%m-%d', 'America/Chicago')

def filter_meetups(meetups):
    now = pendulum.now('America/Chicago')
    three_weeks_out = now.add(weeks=3)
    for meetup in meetups:
        date = meetup_date(meetup)
        if now <= date <= three_weeks_out:
            yield meetup

def add_date_formats(meetups):
    for meetup in meetups:
        date = meetup_date(meetup)
        fmt_date = date.format('%a %b %d')
        meetup['fmt_date'] = fmt_date
        yield meetup
        

@app.route('/digest')
def digest():
    uri = '{API_ROOT}/events'.format(API_ROOT=API_ROOT)
    params = {
        'sign': "true",
        'key': app.config['MEETUP_API_KEY']
    }
    
    response = requests.get(uri, params=params)
    data = response.json()
    
    wrapped_response = list(add_date_formats(filter_meetups(data)))
    return flask.jsonify(wrapped_response)