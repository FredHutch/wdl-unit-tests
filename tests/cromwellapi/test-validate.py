import pytest
from utils import fetch_wdl_paths

wdl_paths = fetch_wdl_paths()


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_validate_good_wdl(cromwell_api, wdl_path):
    """
    Parametrized pytest used to ensure that each WDL unit test passes validation
    with the exception of WDL's that are expected to fail (name starts with "badVal")

    Args:
        cromwell_api (CromwellApi): PROOF server being used to validate WDL unit tests (class defined in cromwell.py)
        wdl_path (PosixPath): location of the WDL script to validate via PROOF
    """
    if not wdl_path.name.startswith("badVal"):
        res = cromwell_api.validate(wdl_path=wdl_path)
        assert isinstance(res, dict)
        assert res["valid"]
        assert res["validWorkflow"]
        assert res["isRunnableWorkflow"]


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_validate_bad_wdl(cromwell_api, wdl_path):
    """
    Parametrized pytest used to ensure that all WDL unit tests that are expected to fail validation
    (name starts with "badVal") actually fail validation via WOMtool.

    Args:
        cromwell_api (CromwellApi): PROOF server being used to validate WDL unit tests (class defined in cromwell.py)
        wdl_path (PosixPath): location of the WDL script to validate via PROOF
    """
    message_check = {
        "badValMissingValue.wdl": "Cannot lookup value 'docker_image'"
    }
    if wdl_path.name.startswith("badVal"):
        res = cromwell_api.validate(wdl_path=wdl_path)
        assert isinstance(res, dict)
        assert not res["valid"]
        assert not res["validWorkflow"]
        assert not res["isRunnableWorkflow"]
        assert message_check[wdl_path.name] in res["errors"][0]
