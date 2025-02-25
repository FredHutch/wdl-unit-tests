import re
import time
from unittest.mock import patch

import pytest
from utils import workflow_states

params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}


@pytest.mark.vcr
def test_failures_initial(cromwell_api, submit_wdls, recording_mode):
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
def test_failures_final(cromwell_api_final, submit_wdls):
    """Checking for failures works for final state"""
    fail = list(filter(lambda x: "badRunParseBatchFile" in x["path"], submit_wdls))
    res = cromwell_api_final.metadata(workflow_id=fail[0]["id"], params=params)
    fail_causedby_mssg = res["failures"][0]["causedBy"][0]["message"]
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
