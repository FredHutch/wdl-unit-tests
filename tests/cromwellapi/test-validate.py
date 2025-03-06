from pathlib import Path

import pytest

root = Path(__file__).parents[2].resolve()
pattern = "**/*.wdl"
wdl_paths = list(root.glob(pattern))


@pytest.mark.vcr
def test_validate_good_wdl(cromwell_api):
    """Checking that validate works - final state is quick"""
    for wdl_path in wdl_paths:
        wdl_name = str(wdl_path).split("/")[-1]
        if not wdl_name.startswith("badVal"):
            res = cromwell_api.validate(wdl_path=wdl_path)
            assert isinstance(res, dict)
            assert res["valid"]
            assert res["validWorkflow"]
            assert res["isRunnableWorkflow"]


@pytest.mark.vcr
def test_validate_bad_wdl(cromwell_api):
    """Checking that validate works - final state is quick"""
    message_check = {"badValMissingValue.wdl": "Cannot lookup value 'docker_image'"}
    for wdl_path in wdl_paths:
        wdl_name = str(wdl_path).split("/")[-1]
        if wdl_name.startswith("badVal"):
            res = cromwell_api.validate(wdl_path=wdl_path)
            assert isinstance(res, dict)
            assert not res["valid"]
            assert not res["validWorkflow"]
            assert not res["isRunnableWorkflow"]
            assert message_check[wdl_name] in res["errors"][0]
