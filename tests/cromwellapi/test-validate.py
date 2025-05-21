import pytest

from ..common_utils import fetch_wdl_paths

wdl_paths_not_bad_val = fetch_wdl_paths(exclude=["badVal"])
wdl_paths_bad_val = fetch_wdl_paths(include=["badVal"])


@pytest.mark.vcr
@pytest.mark.parametrize(
    "wdl_path", wdl_paths_not_bad_val, ids=lambda x: x.name
)
def test_validate_good_wdl(cromwell_api, wdl_path):
    """
    Parametrized pytest used to ensure that each WDL unit test passes validation
    with the exception of WDL's that are expected to fail (name starts with "badVal")

    Cromwell validate route (/api/womtool/v1/describe)

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to validate WDL unit tests (class defined in cromwell.py)
        wdl_path (PosixPath): location of the WDL script to validate via WOMtool
    """
    res = cromwell_api.validate(wdl_path=wdl_path)
    assert isinstance(res, dict)
    assert res["valid"]
    assert res["validWorkflow"]
    assert res["isRunnableWorkflow"]


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths_bad_val, ids=lambda x: x.name)
def test_validate_bad_wdl(cromwell_api, wdl_path):
    """
    Parametrized pytest used to ensure that all WDL unit tests that are expected to fail validation
    (name starts with "badVal") actually fail validation via WOMtool.

    Cromwell validate route (/api/womtool/v1/describe)

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to validate WDL unit tests (class defined in cromwell.py)
        wdl_path (PosixPath): location of the WDL script to validate via WOMtool
    """
    message_check = {"missingValue.wdl": "Cannot lookup value 'docker_image'"}
    res = cromwell_api.validate(wdl_path=wdl_path)
    assert isinstance(res, dict)
    assert not res["valid"]
    assert not res["validWorkflow"]
    assert not res["isRunnableWorkflow"]
    assert message_check[wdl_path.name] in res["errors"][0]
