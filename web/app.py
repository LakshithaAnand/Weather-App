from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys
import requests
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


def daytime(t):
    print('ENTERING daytime')
    if 22 <= t <= 23 or 0 <= t <= 3:
        return "card night"
    elif 10 <= t <= 17:
        return "card day"
    else:
        return "card evening-morning"


def make_dict(name):
    key = '118249e974c33ac4597ba0dd04a9e524'
    req = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=imperial&appid={key}').json()
    weather = {'name': req['name'],
               'temp': req['main']['temp'],
               'state': req['weather'][0]['main'],
               'daytime': daytime((datetime.datetime.utcnow() + datetime.timedelta(seconds=req['timezone'])).hour)}
    return weather


@app.route('/')
def main_page():
    return render_template('index.html', cities=cities)


@app.route('/add', methods=['POST'])
def add_city():
    cities.append(make_dict(request.form["city_name"]))
    return main_page()


cities = [make_dict(city) for city in ("Boston", "New%20York", "Edmonton")]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
