from unittest.mock import patch

import pytest

from ..common_utils import fetch_wdl_paths
from .submit_wdl import submit_wdl

# Parameters included during the PROOF metadata query
# Dictates which fields come through in the response
params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}

wdl_paths_succeed = fetch_wdl_paths(
    exclude=["badRunAPI", "badRunJava", "badVal"]
)


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths_succeed, ids=lambda x: x.name)
def test_successes_initial(cromwell_api, wdl_path, recording_mode, test_name):
    """
    Ensures that each WDL unit test got submitted successfully with the
    exception of WDL's that are expected to fail (name starts with "bad")

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
        wdl_path (str): Path to the WDL file being tested
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api, test_name)

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
@pytest.mark.parametrize("wdl_path", wdl_paths_succeed, ids=lambda x: x.name)
def test_successes_final(
    cromwell_api_final, wdl_path, recording_mode, test_name
):
    """
    Ensures that each WDL unit test executes successfully with the
    exception of WDL's that are expected to fail (name starts with "bad")

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to execute WDL unit tests (class defined in cromwell.py)
        wdl_path (str): Path to the WDL file being tested
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api_final, test_name)

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
