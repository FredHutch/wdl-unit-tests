from unittest.mock import patch

import pytest
from submit_wdl import submit_wdl
from utils import fetch_wdl_paths, metadata_response_keys

params = {"expandSubWorkflows": True}

wdl_paths = fetch_wdl_paths()


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_call_initial(wdl_path, cromwell_api, recording_mode, test_name):
    """Getting workflow metadata with expandSubWorkflows:true works | initial state"""
    job = submit_wdl(wdl_path, recording_mode, cromwell_api, test_name)
    if recording_mode != "rewrite":
        with patch("time.sleep"):
            res = cromwell_api.metadata(job["id"], params=params)
    else:
        res = cromwell_api.metadata(job["id"], params=params)
        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            metadata_response_keys[res["status"].lower()]
        )
        for k, v in res["calls"].items():
            assert (
                v[0]["callCaching"]["effectiveCallCachingMode"]
                == "CallCachingOff"
            )


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_call_final(wdl_path, cromwell_api_final, recording_mode, test_name):
    """Getting workflow metadata with expandSubWorkflows:true works | final state"""
    job = submit_wdl(wdl_path, recording_mode, cromwell_api_final, test_name)
    res = cromwell_api_final.metadata(workflow_id=job["id"], params=params)
    assert isinstance(res, dict)
    assert sorted(list(res.keys())) == sorted(
        metadata_response_keys[res["status"].lower()]
    )
