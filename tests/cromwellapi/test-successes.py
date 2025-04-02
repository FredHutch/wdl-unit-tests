from unittest.mock import patch

import pytest

# Parameters included during the PROOF metadata query
# Dictates which fields come through in the response
params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}


@pytest.mark.vcr
def test_successes_initial(cromwell_api, submit_wdls, recording_mode):
    """
    Ensures that each WDL unit test got submitted successfully with the
    exception of WDL's that are expected to fail (name starts with "bad")

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): PROOF server being used to submit WDL unit tests (class defined in cromwell.py)
        submit_wdls: pytest fixture containing details about WDL submissions to PROOF (defined in conftest.py)
        recording_mode (str): string indicating if the cassettes are getting rewritten or not
    """
    succeed = list(
        filter(lambda x: not x["path"].startswith("bad"), submit_wdls)
    )
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
                # Checking to make sure the workflow hasn't started yet
                # This dictionary represents executions of the individual tasks of the WDL workflow
                assert res["calls"] == {}


@pytest.mark.vcr
def test_successes_final(cromwell_api_final, submit_wdls):
    """
    Ensures that each WDL unit test executes successfully with the
    exception of WDL's that are expected to fail (name starts with "bad")

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): PROOF server being used to execute WDL unit tests (class defined in cromwell.py)
        submit_wdls: pytest fixture containing details about WDL submissions to PROOF (defined in conftest.py)
    """
    succeed = list(
        filter(lambda x: not x["path"].startswith("bad"), submit_wdls)
    )
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
        # Checking to make sure the workflow was actually executed (and not pulled from the cache)
        # If a previous execution is pulled from the cache, this dictionary would be empty
        assert len(res["calls"]) > 0
        assert res["status"] == "Succeeded"
