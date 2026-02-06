from unittest.mock import patch

import pytest

from ..common_utils import fetch_wdl_paths
from .submit_wdl import submit_wdl
from .utils import metadata_response_keys

params = {"expandSubWorkflows": True}

wdl_paths = fetch_wdl_paths()


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_call_initial(wdl_path, cromwell_api, recording_mode, test_name):
    """
    Getting workflow metadata with expandSubWorkflows:true works | initial state

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        wdl_path (str): Path to the WDL file being tested
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    job = submit_wdl(wdl_path, recording_mode, cromwell_api, test_name)
    if recording_mode != "rewrite":
        with patch("time.sleep"):
            res = cromwell_api.metadata(job["id"], params=params)
    else:
        res = cromwell_api.metadata(job["id"], params=params)
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
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_call_final(wdl_path, cromwell_api_final, recording_mode, test_name):
    """
    Getting workflow metadata with expandSubWorkflows:true works | final state

    Cromwell metadata route (/api/workflows/v1/{workflow_id}/metadata)

    Args:
        wdl_path (str): Path to the WDL file being tested
        cromwell_api_final (CromwellApiFinal): Cromwell server being used to check the status of WDL unit tests (class defined in cromwell_final.py)
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        test_name (str): name of the test being run, comes from `ids` parameter of `parametrize`
    """
    job = submit_wdl(wdl_path, recording_mode, cromwell_api_final, test_name)
    res = cromwell_api_final.metadata(workflow_id=job["id"], params=params)
    assert isinstance(res, dict)
    assert set(list(res.keys())).issubset(
        set(metadata_response_keys[res["status"].lower()])
    )
