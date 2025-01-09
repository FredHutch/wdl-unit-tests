import pytest

from utils import metadata_response_keys, workflow_states


@pytest.mark.vcr
def test_metadata(cromwell_api, submit_wdls):
    """Getting workflow metadata works"""
    params = {"expandSubWorkflows": False, "excludeKey": "calls"}
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api.metadata(x, params=params)
        assert isinstance(res, dict)

        if res["status"] in workflow_states["not_final"]:
            assert list(res.keys()) == metadata_response_keys["submitted"]
        elif res["status"] in workflow_states["final"]:
            assert list(res.keys()) == metadata_response_keys["final"]
        else:
            pass
