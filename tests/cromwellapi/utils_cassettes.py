import itertools
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
                dates.append(
                    [
                        parsedate_to_datetime(
                            w["response"]["headers"]["Date"][0]
                        )
                        for w in doc["interactions"]
                    ]
                )
        except FileNotFoundError:
            # This seem very unlikely to happen but just in case
            print(f"file {path} not found")

    if not dates:
        return "unknown"

    all_dates = list(itertools.chain(*dates))
    stamp_mean = sum([w.timestamp() for w in all_dates]) / len(all_dates)
    return datetime.fromtimestamp(stamp_mean).strftime("%B %d, %Y %H:%M")
