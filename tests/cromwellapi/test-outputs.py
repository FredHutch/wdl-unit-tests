import pytest


@pytest.mark.vcr
def test_outputs(cromwell_api, submit_wdls):
    """Getting workflow outputs works"""
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api.outputs(x)
        assert isinstance(res, dict)
        assert list(res.keys()) == [
            "outputs",
            "id",
        ]
