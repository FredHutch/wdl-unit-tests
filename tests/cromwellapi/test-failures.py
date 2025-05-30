import time  # noqa: F401
from unittest.mock import patch

import pytest

from ..common_utils import fetch_wdl_paths
from .submit_wdl import submit_wdl

params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}

wdl_paths_fail = fetch_wdl_paths(include=["badRunAPI", "badVal"])


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths_fail, ids=lambda x: x.name)
def test_failures_initial(cromwell_api, wdl_path, recording_mode, test_name):
    """
    Checking for failures works for initial state

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
            assert res["calls"] == {}


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths_fail, ids=lambda x: x.name)
def test_failures_final(
    cromwell_api_final, wdl_path, recording_mode, test_name
):
    """
    Checking for failures works for final state

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api_final (CromwellApiFinal): Cromwell server being used to check the status of WDL unit tests (class defined in cromwell_final.py)
        wdl_path (str): Path to the WDL file being tested
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api_final, test_name)
    fail_check = {
        "parseBatchFile": "Required workflow input 'parseBatchFile.batchFile' not specified",
        "missingValue": "Cannot lookup value 'docker_image', it is never declared",
    }
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
