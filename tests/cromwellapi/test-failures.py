import time
import re
import pytest
from unittest.mock import patch

from utils import workflow_states


SLEEP_TIME = 5
params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}


@pytest.mark.vcr
def test_failures_initial_state(cromwell_api, submit_wdls, recording_mode):
    """Checking for failures works for initial state"""
    fail = list(filter(lambda x: "badRunParseBatchFile" in x["path"], submit_wdls))

    if recording_mode != "rewrite":
        with patch("time.sleep"):
            res = cromwell_api.metadata(fail[0]["id"], params=params)
    else:
        res = cromwell_api.metadata(fail[0]["id"], params=params)

    assert isinstance(res, dict)

    if len(res) == 0:
        pytest.skip("call to /metadata route gave empty response")
    else:
        status = res.get("status", "")
        if status == "Submitted":
            assert sorted(list(res.keys())) == sorted(
                [
                    "status",
                    "calls",
                    "id",
                ]
            )
            assert res["calls"] == {}


@pytest.mark.vcr
def test_failures_final_state(cromwell_api, submit_wdls, recording_mode):
    """Checking for failures works for final state"""
    fail = list(filter(lambda x: "badRunParseBatchFile" in x["path"], submit_wdls))
    # print(f"fail0: {fail[0]}")

    not_final = True
    while not_final:
        time.sleep(SLEEP_TIME if recording_mode == "rewrite" else 0)
        res = cromwell_api.metadata(fail[0]["id"], params=params)
        if res.get("status") is not None:
            not_final = res.get("status").lower() not in [
                x.lower() for x in workflow_states["final"]
            ]

    # print(f"cromwell_api.metadata output:{res}")

    fail_causedby_mssg = res["failures"][0]["causedBy"][0]["message"]
    # fail_mssg = res["failures"]["message"]
    assert isinstance(res, dict)
    assert sorted(list(res.keys())) == sorted(
        [
            "status",
            "failures",
            "calls",
            "id",
        ]
    )
    assert re.search("not specified", fail_causedby_mssg) is not None
    # assert re.search("failed", fail_mssg) is not None
