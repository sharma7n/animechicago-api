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

@app.route('/digest')
def digest():
    uri = '{API_ROOT}/events'.format(API_ROOT=API_ROOT)
    params = {
        'sign': "true",
        'key': app.config['MEETUP_API_KEY']
    }
    
    response = requests.get(uri, params=params)
    data = response.json()
    now = pendulum.now('America/Chicago')
    three_weeks_out = now.add(weeks=3)
    filtered_data = [
        record for record in data 
        if now <= pendulum.from_format(record['local_date'], '%Y-%m-%d') <= three_weeks_out
    ]
    
    return flask.jsonify(filtered_data)