from unittest.mock import patch

import pytest
from utils import metadata_response_keys

params = {"expandSubWorkflows": True}


@pytest.mark.vcr
def test_call_initial(cromwell_api, submit_wdls, recording_mode):
    """Getting workflow metadata with expandSubWorkflows:true works | initial state"""
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        if recording_mode != "rewrite":
            with patch("time.sleep"):
                res = cromwell_api.metadata(x, params=params)
        else:
            res = cromwell_api.metadata(x, params=params)

        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            metadata_response_keys[res["status"].lower()]
        )


@pytest.mark.vcr
def test_call_final(cromwell_api_final, submit_wdls):
    """Getting workflow metadata with expandSubWorkflows:true works | final state"""
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api_final.metadata(workflow_id=x, params=params)
        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            metadata_response_keys[res["status"].lower()]
        )
