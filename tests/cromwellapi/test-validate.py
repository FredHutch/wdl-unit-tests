from pathlib import Path

import pytest

root = Path(__file__).parents[2].resolve()
pattern = "**/*.wdl"
wdl_paths = list(root.glob(pattern))


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_validate_good_wdl(cromwell_api, wdl_path):
    """Checking that validate works - final state is quick"""
    if not wdl_path.name.startswith("badVal"):
        res = cromwell_api.validate(wdl_path=wdl_path)
        assert isinstance(res, dict)
        assert res["valid"]
        assert res["validWorkflow"]
        assert res["isRunnableWorkflow"]


@pytest.mark.vcr
@pytest.mark.parametrize("wdl_path", wdl_paths, ids=lambda x: x.name)
def test_validate_bad_wdl(cromwell_api, wdl_path):
    """Checking that validate works - final state is quick"""
    message_check = {"badValMissingValue.wdl": "Cannot lookup value 'docker_image'"}
    if wdl_path.name.startswith("badVal"):
        res = cromwell_api.validate(wdl_path=wdl_path)
        assert isinstance(res, dict)
        assert not res["valid"]
        assert not res["validWorkflow"]
        assert not res["isRunnableWorkflow"]
        assert message_check[wdl_path.name] in res["errors"][0]
