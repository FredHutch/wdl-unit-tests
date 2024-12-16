import os

import httpx

BASE_URL = "https://proof-api-dev.fredhutch.org"
# test user token
TOKEN = os.getenv("PROOF_API_TOKEN_DEV")
headers = {"Authorization": f"Bearer {TOKEN}"}
info_keys = ["branch", "commit_sha", "short_commit_sha", "commit_message", "tag"]
status_keys = [
    "canJobStart",
    "jobStatus",
    "cromwellUrl",
    "jobStartTime",
    "jobEndTime",
    "jobInfo",
]


def test_info():
    res = httpx.get(f"{BASE_URL}/info")
    assert isinstance(res, httpx.Response)
    assert list(res.json().keys()) == info_keys


def test_status():
    res = httpx.get(f"{BASE_URL}/cromwell-server", headers=headers, timeout=10)
    assert isinstance(res, httpx.Response)
    assert list(res.json().keys()) == status_keys
