import os
from pathlib import Path

PROOF_BASE_URL = "https://proof-api-dev.fredhutch.org"
TOKEN = os.getenv("PROOF_API_TOKEN_DEV")


def make_path(file):
    path = Path(__file__).parents[2].resolve()
    return path / f"{file}/{file}.wdl"
