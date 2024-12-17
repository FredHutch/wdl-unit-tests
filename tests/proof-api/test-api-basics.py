import httpx
from constants import BASE_URL, TOKEN

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
