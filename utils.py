import argparse
from typing import Any


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


def get_artist_hint(artist_info: dict) -> str:
    """Returns a hint for the artist's name."""
    return_str = ""
    if artist_info["categories"] is not None:
        return_str += f"This {', '.join(artist_info['categories'])} is from {artist_info['location_city']}. "
    if artist_info['bio_birthdate'] is not None:
        return_str += f"They were born on {artist_info['bio_birthdate']}. "
    if artist_info['bio_yearsactivestart'] is not None:
        return_str += f"They began their career in {artist_info['bio_yearsactivestart']}. "
    if artist_info['spotify_genres'] is not None:
        return_str += f"They are known for their {', '.join(artist_info['spotify_genres'])}. "
    if artist_info["spotify_top_tracks"] is not None:
        return_str += f"Their top tracks are {', '.join([track['name'] for track in artist_info['spotify_top_tracks']['tracks']])}. "
    return return_str
