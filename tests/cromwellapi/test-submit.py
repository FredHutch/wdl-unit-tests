from utils import path_wdl, path_options


def test_submit_works(cromwell_api):
    """Submitting a WDL file works"""
    res = cromwell_api.submit_workflow(
        wdl_path=path_wdl("helloHostname"), options=path_options("helloHostname")
    )
    assert isinstance(res, dict)
    assert res["status"] == "Submitted"
