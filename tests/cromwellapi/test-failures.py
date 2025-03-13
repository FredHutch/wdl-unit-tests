import time  # noqa: F401
from unittest.mock import patch

import pytest
from submit_wdl import submit_wdl
from utils import fetch_wdl_paths

params = {
    "includeKey": [
        "status",
        "failures",
        "jobId",
    ]
}


wdl_paths = fetch_wdl_paths()
wdl_paths_fail = list(
    filter(lambda x: any([w.startswith("bad") for w in x.parts]), wdl_paths)
)


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths_fail, ids=lambda x: x.name)
def test_failures_initial(cromwell_api, wdl_path, recording_mode, test_name):
    """Checking for failures works for initial state"""
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
    """Checking for failures works for final state"""
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api_final, test_name)

    fail_check = {
        "badRunParseBatchFile": "Required workflow input 'parseBatchFile.batchFile' not specified",
        "badValMissingValue": "Cannot lookup value 'docker_image', it is never declared",
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
