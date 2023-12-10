import json
from random import sample
from flask import Flask, request, make_response
from flask import render_template
from data.cities import CITIES
from utils import get_artist_hint
from data.artist_types import ARTIST_TYPES

# -----------------------------------------------------------------------
app = Flask(__name__, template_folder="templates")
DATA_PATH = 'data/rappers_w_spotify.json'
EASY_ARTISTS_PATH = 'data/easy_rappers_w_spotify.json'


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
    if mode == "hard":
        data_path = DATA_PATH
    else:
        data_path = EASY_ARTISTS_PATH
    with open(data_path, 'r') as file:
        data = json.load(file)
    markers = []
    names = []
    for i, element in enumerate(sample(data, 5)):
        markers.append({
            'lat': element['location_coordinates']['lat'],
            'lon': element['location_coordinates']['lon'],
            'popup': str(i + 1) + ": " + get_artist_hint(element),
            'image': element['spotify_images'][0]['url']
        })
        names.append(element['name'])
    return render_template('game.html', markers=markers, lat=40.7128, lon=74.0060, mode=mode,
                           next_mode=mode_map[mode], names=names)


@app.route("/study", methods=["GET"])
def study():
    markers = []
    with open(DATA_PATH, 'r') as file:
        data = json.load(file)
    location = request.args.get('location')
    artist_type = request.args.get('artist_type')
    popularity = request.args.get('popularity')
    for element in data:
        if location is not None and len(location) > 0 and location != element['location_city']:
            continue
        if artist_type is not None and len(artist_type) > 0 is not None and element[
            'categories'] is not None and artist_type not in element['categories']:
            continue
        if popularity is not None and element["spotify_popularity"] < int(popularity):
            continue
        popularity = int(popularity) if popularity is not None else None
        markers.append({
            'lat': element['location_coordinates']['lat'],
            'lon': element['location_coordinates']['lon'],
            'popup': element['name'] + ": " + element["bio_summary"],
            'video': element["youtube_clipexampleurl"]
        })
    return render_template('study.html',
                           markers=markers, lat=40.7128, lon=74.0060, cities=CITIES,
                           artist_types=ARTIST_TYPES, loc=location, artist_type=artist_type, pop=popularity)
