from utils import make_path


def test_submit_works(cromwell_api):
    """Submitting a WDL file works"""
    res = cromwell_api.submit_workflow(wdl_path=make_path("helloHostname"))
    assert isinstance(res, dict)
    assert res["status"] == "Submitted"
