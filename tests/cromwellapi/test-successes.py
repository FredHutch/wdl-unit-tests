import time
import re
import pytest
from unittest.mock import patch

from utils import workflow_states


params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}


@pytest.mark.vcr
def test_successes_initial(cromwell_api, submit_wdls, recording_mode):
    """Checking for failures works for initial state"""
    succeed = list(filter(lambda x: not x["path"].startswith("bad"), submit_wdls))
    for job in succeed:
        if recording_mode != "rewrite":
            with patch("time.sleep"):
                res = cromwell_api.metadata(job["id"], params=params)
        else:
            res = cromwell_api.metadata(job["id"], params=params)
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
def test_successes_final(cromwell_api_final, submit_wdls):
    """Checking for failures works for final state"""
    succeed = list(filter(lambda x: not x["path"].startswith("bad"), submit_wdls))
    for job in succeed:
        res = cromwell_api_final.metadata(workflow_id=job["id"], params=params)
        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            [
                "status",
                "calls",
                "id",
            ]
        )
        assert len(res["calls"]) > 0
        assert res["status"] == "Succeeded"
