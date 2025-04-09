import pytest
from submit_wdl import submit_wdl
from utils import fetch_wdl_paths, metadata_response_keys

params = {"expandSubWorkflows": False, "excludeKey": "calls"}

wdl_paths = fetch_wdl_paths()


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_metadata_initial(cromwell_api, wdl_path, recording_mode, test_name):
    """Getting workflow metadata works - Initial states"""
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api, test_name)

    res = cromwell_api.metadata(workflow_id=job["id"], params=params)
    assert isinstance(res, dict)
    assert sorted(list(res.keys())) == sorted(
        metadata_response_keys[res["status"].lower()]
    )


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_metadata_final(
    cromwell_api_final, wdl_path, recording_mode, test_name
):
    """Getting workflow metadata works - Final states"""
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api_final, test_name)

    res = cromwell_api_final.metadata(workflow_id=job["id"], params=params)
    assert isinstance(res, dict)
    assert sorted(list(res.keys())) == sorted(
        metadata_response_keys[res["status"].lower()]
    )
