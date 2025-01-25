import pytest
from unittest.mock import patch

from utils import metadata_response_keys, workflow_states


@pytest.mark.vcr
def test_call(cromwell_api, submit_wdls, recording_mode):
    """Getting workflow metadata with expandSubWorkflows:true works"""
    params = {"expandSubWorkflows": True}
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        if recording_mode != "rewrite":
            with patch("time.sleep"):
                res = cromwell_api.metadata(x, params=params)
        else:
            res = cromwell_api.metadata(x, params=params)

        assert isinstance(res, dict)

        if res["status"] in workflow_states["not_final"]:
            assert list(res.keys()) == metadata_response_keys["submitted"]
        elif res["status"] in workflow_states["final"]:
            assert list(res.keys()) == metadata_response_keys["final"]
        else:
            pass
