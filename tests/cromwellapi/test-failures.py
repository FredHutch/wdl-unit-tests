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
def test_failures_initial(cromwell_api, submit_wdls, recording_mode):
    """Checking for failures works for initial state"""
    fail = list(filter(lambda x: x["path"].startswith("bad"), submit_wdls))
    for job in fail:
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
def test_failures_final(cromwell_api_final, submit_wdls):
    """Checking for failures works for final state"""
    fail = list(filter(lambda x: x["path"].startswith("bad"), submit_wdls))
    fail_check = {"badRunParseBatchFile":"Required workflow input 'parseBatchFile.batchFile' not specified",
                  "badValMissingValue":"Cannot lookup value 'docker_image', it is never declared"}
    for job in fail:
        res = cromwell_api_final.metadata(workflow_id=job["id"], params=params)
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
        assert len(res["calls"]) > 0
        wdl_name = job["path"].split("/")[0]
        if wdl_name in fail_check:
            assert fail_check[wdl_name] in fail_causedby_mssg
