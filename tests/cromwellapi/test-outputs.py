import pytest


@pytest.mark.vcr
def test_outputs(cromwell_api, submit_wdls):
    """
    Getting workflow outputs works

    Cromwell outputs route (/api/workflows/v1/{workflow_id}/outputs)

    Args:
        cromwell_api (CromwellApi): PROOF server being used to submit WDL unit tests (class defined in cromwell.py)
        recording_mode (str): string indicating if the cassettes are getting rewritten or not
    """
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api.outputs(x)
        assert isinstance(res, dict)
        assert list(res.keys()) == [
            "outputs",
            "id",
        ]
