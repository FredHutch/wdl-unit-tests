import pytest
from utils import path_options, path_wdl

wdls = ["helloHostname", "helloDockerHostname"]


@pytest.mark.vcr
@pytest.mark.parametrize("wdl", wdls)
def test_abort(cromwell_api, wdl):
    """Checking that abort works"""
    workflow = cromwell_api.submit_workflow(
        wdl_path=path_wdl(wdl), options=path_options(wdl)
    )
    aborted = cromwell_api.abort(workflow["id"])
    assert isinstance(aborted, dict)
    assert aborted["status"] == "Aborted"
