import pytest
from submit_wdl import submit_wdl
from utils import fetch_wdl_paths

wdl_paths = fetch_wdl_paths()


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_outputs(cromwell_api, wdl_path, recording_mode, test_name):
    """
    Getting workflow outputs works

    Cromwell outputs route (/api/workflows/v1/{workflow_id}/outputs)

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
        wdl_path (str): Path to the WDL file being tested
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    job = submit_wdl(wdl_path, recording_mode, cromwell_api, test_name)

    res = cromwell_api.outputs(job["id"])
    assert isinstance(res, dict)
    assert list(res.keys()) == [
        "outputs",
        "id",
    ]
