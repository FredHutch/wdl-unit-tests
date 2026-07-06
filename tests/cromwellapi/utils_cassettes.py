from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

import yaml


def list_cassettes(directory):
    """List all cassette files

    Examples:
        list_cassettes(dir="tests/cromwellapi/cassettes")
    """
    cassette_path = Path(directory)
    return [str(file) for file in cassette_path.glob("**/*.yaml")]


def cassettes_last_modified(directory):
    """Get a single last modified date across all cassettes

    Examples:
        cassettes_last_modified(dir="tests/cromwellapi/cassettes")
        cassettes_last_modified(dir="tests/cromwellapi/notfound")
    """
    cassettes = list_cassettes(directory)
    dates = []
    for path in cassettes:
        try:
            with open(path, "r") as f:
                doc = yaml.load(f, Loader=yaml.SafeLoader)
                for w in doc["interactions"]:
                    try:
                        date = w["response"]["headers"]["Date"][0]
                    except KeyError:
                        date = w["response"]["headers"]["date"][0]

                    dates.append(parsedate_to_datetime(date))

        except FileNotFoundError:
            # This seem very unlikely to happen but just in case
            print(f"file {path} not found")

    if not dates:
        return "unknown"

    stamp_mean = sum([w.timestamp() for w in dates]) / len(dates)
    return datetime.fromtimestamp(stamp_mean).strftime("%B %d, %Y %H:%M")
