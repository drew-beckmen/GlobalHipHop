import json
JSON_FILE = 'rappers.json'


def main():
    with open(JSON_FILE, 'r') as file:
        data = json.load(file)

    cities = set()
    for rapper in data:
        categories = rapper['categories']
        if categories is None:
            continue
        for category in categories:
            cities.add(category)
    sorted = list(cities)
    sorted.sort()
    for city in sorted:
        print("'" + city + "',")


if __name__ == "__main__":
    main()

