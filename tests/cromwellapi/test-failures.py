import time  # noqa: F401
from unittest.mock import patch

import pytest

params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}


@pytest.mark.vcr
def test_failures_initial(cromwell_api, submit_wdls, recording_mode):
    """
    Checking for failures works for initial state

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): PROOF server being used to submit WDL unit tests (class defined in cromwell.py)
        submit_wdls: pytest fixture containing details about WDL submissions to PROOF (defined in conftest.py)
        recording_mode (str): string indicating if the cassettes are getting rewritten or not
    """
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
    """
    Checking for failures works for final state

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api_final (CromwellApiFinal): PROOF server being used to check the status of WDL unit tests (class defined in cromwell_final.py)
        submit_wdls: pytest fixture containing details about WDL submissions to PROOF (defined in conftest.py)
    """
    fail = list(filter(lambda x: x["path"].startswith("bad"), submit_wdls))
    fail_check = {
        "badRunParseBatchFile": "Required workflow input 'parseBatchFile.batchFile' not specified",
        "badValMissingValue": "Cannot lookup value 'docker_image', it is never declared",
    }
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
        wdl_name = job["path"].split("/")[0]
        if wdl_name in fail_check:
            assert fail_check[wdl_name] in fail_causedby_mssg
