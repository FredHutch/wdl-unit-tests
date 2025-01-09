import pytest

from utils import make_path


@pytest.mark.vcr
def test_submit_works(cromwell_api):
    """Submitting a WDL file works"""
    res = cromwell_api.submit_workflow(wdl_path=make_path("helloHostname"))
    assert isinstance(res, dict)
    assert res["status"] == "Submitted"
