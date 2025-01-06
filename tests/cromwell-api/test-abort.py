import pytest

from utils import make_path

wdls = ["helloHostname", "helloDockerHostname", "helloModuleHostname"]


@pytest.mark.parametrize("wdl", wdls)
def test_abort(cromwell_api, wdl):
    """Checking that abort works"""
    workflow = cromwell_api.submit_workflow(wdl_path=make_path(wdl))
    aborted = cromwell_api.abort(workflow["id"])
    assert isinstance(aborted, dict)
    assert aborted["status"] == "Aborted"
