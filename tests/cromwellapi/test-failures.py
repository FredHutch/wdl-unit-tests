# import re
import pytest


@pytest.mark.vcr
def test_failures_initial_state(cromwell_api, submit_wdls):
    """Checking for failures works for initial state"""
    params = {"includeKey": "failures", "includeKey": "jobId"}
    fail = list(filter(lambda x: "badRunParseBatchFile" in x["path"], submit_wdls))
    res = cromwell_api.metadata(fail[0]["id"], params=params)
    assert isinstance(res, dict)
    assert res == {}


# def test_failures_final_state(cromwell_api, submit_wdls):
#     """Checking for failures works for final state"""
#     params = {"includeKey": "failures", "includeKey": "jobId"}
#     fail = list(filter(lambda x: "badRunParseBatchFile" in x["path"], submit_wdls))
#     print(f"fail0: {fail[0]}")
#     res = cromwell_api.metadata(fail[0]["id"], params=params)
#     print(f"cromwell_api.metadata output:{res}")
#     fail_causedby_mssg = res["failures"]["causedBy"]["message"]
#     fail_mssg = res["failures"]["message"]
#     assert isinstance(res, dict)
#     assert list(res.keys()) == [
#         "failures",
#         "calls",
#         "id",
#     ]
#     assert re.search("not specified", fail_causedby_mssg) is not None
#     assert re.search("failed", fail_mssg) is not None
