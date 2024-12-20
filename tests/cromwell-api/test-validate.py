from utils import make_path


def test_validate_good_wdl(cromwell_api):
    """Checking that validate works - final state is quick"""
    res = cromwell_api.validate(wdl_path=make_path("helloHostname"))
    assert isinstance(res, dict)
    assert res["valid"]
    assert res["validWorkflow"]
    assert res["isRunnableWorkflow"]


def test_validate_bad_wdl(cromwell_api):
    """Checking that validate works - final state is quick"""
    res = cromwell_api.validate(wdl_path=make_path("badFile"))
    assert isinstance(res, dict)
    assert not res["valid"]
    assert not res["validWorkflow"]
    assert not res["isRunnableWorkflow"]
    assert "Cannot lookup value 'docker_image'" in res["errors"][0]
