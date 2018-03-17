import os

import flask
import flask_cors
import pendulum
import requests
import untangle

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['MEETUP_API_KEY'] = os.environ['MEETUP_API_KEY']
flask_cors.CORS(app)

API_ROOT = 'https://api.meetup.com/animechicago'

def filter_meetups(meetups):
    now = pendulum.now('America/Chicago')
    three_weeks_out = now.add(weeks=3)
    for meetup in meetups:
        date = pendulum.from_format(
            meetup['local_date'], 
            '%Y-%m-%d', 
            'America/Chicago')
            
        if now <= date <= three_weeks_out:
            yield meetup

@app.route('/meetups')
def meetups():
    response = requests.get(f'{API_ROOT}/events', params={
        'sign': "true",
        'key': app.config['MEETUP_API_KEY']
    })
    
    data = response.json()
    return flask.jsonify(list(filter_meetups(data)))

@app.route('/events')
def events():
    events = untangle.parse('https://animechicago.com/feed/?topic=events')
    items = events.rss.channel.item
    data = [
        {
            'title': item.title.cdata,
            'link': item.link.cdata,
            'description': item.description.cdata
        }
        for item in items
    ]
    
    return flask.jsonify(data)