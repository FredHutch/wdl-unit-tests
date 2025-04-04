from unittest.mock import patch

import pytest
from utils import metadata_response_keys

params = {"expandSubWorkflows": True}


@pytest.mark.vcr
def test_call_initial(cromwell_api, submit_wdls, recording_mode):
    """
    Getting workflow metadata with expandSubWorkflows:true works | initial state

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api (CromwellApi): PROOF server being used to submit WDL unit tests (class defined in cromwell.py)
        submit_wdls: pytest fixture containing details about WDL submissions to PROOF (defined in conftest.py)
        recording_mode (str): string indicating if the cassettes are getting rewritten or not
    """
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        if recording_mode != "rewrite":
            with patch("time.sleep"):
                res = cromwell_api.metadata(x, params=params)
        else:
            res = cromwell_api.metadata(x, params=params)

        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            metadata_response_keys[res["status"].lower()]
        )
        for k, v in res["calls"].items():
            assert (
                v[0]["callCaching"]["effectiveCallCachingMode"]
                == "CallCachingOff"
            )


@pytest.mark.vcr
def test_call_final(cromwell_api_final, submit_wdls):
    """
    Getting workflow metadata with expandSubWorkflows:true works | final state

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        cromwell_api_final (CromwellApiFinal): PROOF server being used to check the status of WDL unit tests (class defined in cromwell_final.py)
        submit_wdls: pytest fixture containing details about WDL submissions to PROOF (defined in conftest.py)
    """
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api_final.metadata(workflow_id=x, params=params)
        assert isinstance(res, dict)
        assert sorted(list(res.keys())) == sorted(
            metadata_response_keys[res["status"].lower()]
        )
        for k, v in res["calls"].items():
            assert (
                v[0]["callCaching"]["effectiveCallCachingMode"]
                == "CallCachingOff"
            )
