import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

JSON_FILE = 'rappers.json'
OUTPUT_FILE = 'rappers_w_spotify.json'
CLIENT_ID = '1401a6a765b144819acd000af10880f7'
CLIENT_SECRET = '24f64877b3044d0b899b4a0dde616896'

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)
    new_data = []
    length = len(data)
    for i, element in enumerate(data):
        print(f"Processing {i + 1}/{length}")
        if 'spotify_id' in element:
            continue
        artist_name = element['name']
        if ' ' in artist_name:
            artist_name = artist_name.split(' ')[0]
        results = sp.search(q='artist:' + artist_name, type='artist')
        if len(results['artists']['items']) == 0:
            continue

        # Don't just take the first result, take the first result that matches the name
        changed = False
        for artist in results['artists']['items']:
            if artist['name'] == element['name']:
                results['artists']['items'] = [artist]
                changed = True
                break
        if not changed:
            continue
        # At this point, we have valid artist data from Spotify
        element['spotify_id'] = results['artists']['items'][0]['id']
        element['spotify_url'] = results['artists']['items'][0]['external_urls']['spotify']
        element['spotify_followers'] = results['artists']['items'][0]['followers']['total']
        element['spotify_popularity'] = results['artists']['items'][0]['popularity']
        element['spotify_genres'] = results['artists']['items'][0]['genres']
        element['spotify_images'] = results['artists']['items'][0]['images']

        id = results['artists']['items'][0]['id']
        # Search for artists top tracks
        top_tracks = sp.artist_top_tracks(id)
        element['spotify_top_tracks'] = top_tracks
        new_data.append(element)

    # Dump the data to a new file
    with open(OUTPUT_FILE, 'w') as file:
        json.dump(new_data, file)


if __name__ == "__main__":
    main()
