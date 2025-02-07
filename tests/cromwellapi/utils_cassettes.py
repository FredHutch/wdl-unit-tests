import yaml
import itertools
from pathlib import Path
from datetime import datetime
import dateparser


def list_cassettes(dir):
    """List all cassette files

    Examples:
        list_cassettes(dir="tests/cromwellapi/cassettes")
    """
    cassette_path = Path(dir)
    return [str(file) for file in cassette_path.glob("**/*.yaml")]


def cassettes_last_modified(dir):
    """Get a single last modified date across all cassettes

    Examples:
        cassettes_last_modified(dir="tests/cromwellapi/cassettes")
        cassettes_last_modified(dir="tests/cromwellapi/notfound")
    """
    cassettes = list_cassettes(dir)
    dates = []
    for path in cassettes:
        try:
            with open(path, "r") as f:
                doc = yaml.load(f, Loader=yaml.SafeLoader)
                dates.append(
                    [
                        dateparser.parse(int["response"]["headers"]["Date"][0])
                        for int in doc["interactions"]
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
