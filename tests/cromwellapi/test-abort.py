import pytest

from utils import path_wdl, path_options

wdls = ["helloHostname", "helloDockerHostname", "helloModuleHostname"]


@pytest.mark.parametrize("wdl", wdls)
def test_abort(cromwell_api, wdl):
    """Checking that abort works"""
    workflow = cromwell_api.submit_workflow(
        wdl_path=path_wdl(wdl), options=path_options(wdl)
    )
    aborted = cromwell_api.abort(workflow["id"])
    assert isinstance(aborted, dict)
    assert aborted["status"] == "Aborted"
