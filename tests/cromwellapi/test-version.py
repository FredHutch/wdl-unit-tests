import pytest


@pytest.mark.vcr
def test_version(cromwell_api):
    res = cromwell_api.version()
    assert isinstance(res, dict)
