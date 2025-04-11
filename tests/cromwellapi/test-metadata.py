import pytest
from utils import metadata_response_keys

params = {"expandSubWorkflows": False, "excludeKey": "calls"}


@pytest.mark.vcr
def test_metadata_initial(cromwell_api, submit_wdls):
    """
    Getting workflow metadata works - Initial states

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
        recording_mode (str): string indicating if the cassettes are getting rewritten or not
    """
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api.metadata(workflow_id=x, params=params)
        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            metadata_response_keys[res["status"].lower()]
        )


@pytest.mark.vcr
def test_metadata_final(cromwell_api_final, submit_wdls):
    """
    Getting workflow metadata works - Final states

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api_final (CromwellApiFinal): Cromwell server being used to check the status of WDL unit tests (class defined in cromwell_final.py)
        submit_wdls: pytest fixture containing details about WDL submissions to PROOF (defined in conftest.py)
    """
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api_final.metadata(workflow_id=x, params=params)
        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            metadata_response_keys[res["status"].lower()]
        )
