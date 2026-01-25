import json
from pathlib import Path

DATA_FOLDER = "data"


def _json_from_file(filename, key):
    """Helper method - loads JSON from 'filename' and return whatever is at the 'key'"""
    filepath = Path(__file__).parent / DATA_FOLDER / filename
    with open(filepath) as fp:
        data = json.load(fp)
        return data[key]


def _save_json_to_file(filename, key, data):
    """Helper method - saves JSON data back to 'filename' under 'key'"""
    filepath = Path(__file__).parent / DATA_FOLDER / filename
    with open(filepath, "w") as fp:
        json.dump({key: data}, fp, indent=4)


def get_clubs():
    """Load clubs from JSON"""
    return _json_from_file("clubs.json", "clubs")


def get_competitions():
    """Load competitions from JSON"""
    return _json_from_file("competitions.json", "competitions")


def save_competitions(competitions):
    """Persist updated competitions to JSON"""
    _save_json_to_file("competitions.json", "competitions", competitions)
