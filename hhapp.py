import json
from flask import Flask, request, make_response
from flask import render_template
from data.cities import CITIES
from data.artist_types import ARTIST_TYPES

# -----------------------------------------------------------------------
app = Flask(__name__, template_folder="templates")
DATA_PATH = 'data/rappers.json'


# Index endpoint is the main page of the app
@app.route("/", methods=["GET"])
def index():
    html = render_template("index.html")
    response = make_response(html)
    return response


@app.route("/game", methods=["GET"])
def game():
    mode = request.args.get('mode')
    if mode is None:
        mode = "easy"
    mode_map = {
        "easy": "hard",
        "hard": "easy"
    }
    markers = [
        {
            'lat': 0,
            'lon': 0,
            'popup': 'This is the middle of the map.'
        }
    ]
    return render_template('game.html', markers=markers, lat=40.7128, lon=74.0060, mode=mode, next_mode=mode_map[mode])


@app.route("/study", methods=["GET"])
def study():
    markers = []
    with open(DATA_PATH, 'r') as file:
        data = json.load(file)
    location = request.args.get('location')
    artist_type = request.args.get('artist_type')
    print(location, artist_type == "")
    for element in data:
        if len(location) > 0 and location != element['location_city']:
            continue
        if len(artist_type) > 0 is not None and element['categories'] is not None and artist_type not in element['categories']:
            continue
        markers.append({
            'lat': element['location_coordinates']['lat'],
            'lon': element['location_coordinates']['lon'],
            'popup': element['name'] + ": " + element["bio_summary"],
            'video': element["youtube_clipexampleurl"]
        })
    return render_template('study.html', markers=markers, lat=40.7128, lon=74.0060, cities=CITIES, artist_types=ARTIST_TYPES)
