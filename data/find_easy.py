import json

DATA_PATH = './rappers_w_spotify.json'
EASY_ARTISTS_PATH = './easy_rappers_w_spotify.json'

final_result = []
with open(DATA_PATH, 'r') as file:
    data = json.load(file)

print(len(data))
for element in data:
    if element["spotify_popularity"] > 70:
        final_result.append(element)
        print("Adding to popular")

with open(EASY_ARTISTS_PATH, 'w') as file:
    json.dump(final_result, file)
