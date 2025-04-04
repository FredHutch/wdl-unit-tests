import pytest
from utils import path_options, path_wdl


@pytest.mark.vcr
def test_submit_works(cromwell_api):
    """
    Submitting a WDL file works

    Cromwell submission route (/api/workflows/v1)

    Args:
        cromwell_api (CromwellApi): PROOF server being used to submit WDL unit tests (class defined in cromwell.py)
    """
    res = cromwell_api.submit_workflow(
        wdl_path=path_wdl("helloHostname"),
        options=path_options("helloHostname"),
    )
    assert isinstance(res, dict)
    assert res["status"] == "Submitted"
