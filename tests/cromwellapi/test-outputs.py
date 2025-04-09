import pytest
from submit_wdl import submit_wdl
from utils import fetch_wdl_paths

wdl_paths = fetch_wdl_paths()


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_outputs(cromwell_api, wdl_path, recording_mode, test_name):
    """Getting workflow outputs works"""
    job = submit_wdl(wdl_path, recording_mode, cromwell_api, test_name)

    res = cromwell_api.outputs(job["id"])
    assert isinstance(res, dict)
    assert list(res.keys()) == [
        "outputs",
        "id",
    ]
