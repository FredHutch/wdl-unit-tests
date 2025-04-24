import pytest


@pytest.mark.vcr
def test_version(cromwell_api):
    """
    Test the Cromwell version endpoint (/engine/v1/version)

    We're not testing exact version number as we just care about the data type

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
    """

    res = cromwell_api.version()
    assert isinstance(res, dict)
