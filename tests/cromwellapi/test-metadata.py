import pytest

from .submit_wdl import submit_wdl
from .utils import fetch_wdl_paths, metadata_response_keys

params = {"expandSubWorkflows": False, "excludeKey": "calls"}

wdl_paths = fetch_wdl_paths()


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_metadata_initial(cromwell_api, wdl_path, recording_mode, test_name):
    """
    Getting workflow metadata works - Initial states

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
        wdl_path (str): Path to the WDL file being tested
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api, test_name)

    res = cromwell_api.metadata(workflow_id=job["id"], params=params)
    assert isinstance(res, dict)
    assert sorted(list(res.keys())) == sorted(
        metadata_response_keys[res["status"].lower()]
    )


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_metadata_final(
    cromwell_api_final, wdl_path, recording_mode, test_name
):
    """
    Getting workflow metadata works - Final states

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api_final (CromwellApiFinal): Cromwell server being used to check the status of WDL unit tests (class defined in cromwell_final.py)
        wdl_path (str): Path to the WDL file being tested
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    print(f"Current test name: {test_name}")
    job = submit_wdl(wdl_path, recording_mode, cromwell_api_final, test_name)

    res = cromwell_api_final.metadata(workflow_id=job["id"], params=params)
    assert isinstance(res, dict)
    assert sorted(list(res.keys())) == sorted(
        metadata_response_keys[res["status"].lower()]
    )
