import argparse
from typing import Any
from geopy.geocoders import Nominatim

def initialize_argparse(
        desc: str, positionals: Any | list[tuple] = None, optionals: Any | dict = None
) -> argparse.ArgumentParser:
    """Initializes an ArgumentParser to accept arguments defined in props."""

    parser = argparse.ArgumentParser(description=desc)

    for pos_arg, pos_help in positionals or list():
        parser.add_argument(pos_arg, help=pos_help)

    for argument in optionals or dict():
        arg_data = optionals[argument]
        parser.add_argument(f"-{argument}", metavar=arg_data[0], help=arg_data[1])

    return parser


def get_location_of(coo: str, data: dict[str, str]) -> tuple[str, str, str]:
    """Function to get the country of given coordinates.

    Args:
        coo: coordinates as string ("lat, lon").
        data: input dictionary of countries and continents.

    Returns:
        Tuple of coordinates, country and continent (or Unknown if country not found).

    """
    geolocator = Nominatim(user_agent="stackoverflow", timeout=25)
    country: str = (
        geolocator.reverse(coo, language="en-US").raw["display_name"].split(", ")[-1]
    )
    return (coo, country, data.get(country, "Unknown"))
