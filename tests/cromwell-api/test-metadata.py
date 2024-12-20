meta_keys_state_submitted = [
    "submittedFiles",
    "calls",
    "outputs",
    "status",
    "id",
    "inputs",
    "labels",
    "submission",
]
meta_keys_state_final = [
    "workflowName",
    "workflowProcessingEvents",
    "actualWorkflowLanguageVersion",
    "submittedFiles",
    "calls",
    "outputs",
    "workflowRoot",
    "actualWorkflowLanguage",
    "status",
    "end",
    "start",
    "id",
    "inputs",
    "labels",
    "submission",
]
states_not_final = [
    "Running",
    "Submitted",
    "Pending",
]
states_final = [
    "Failed",
    "Aborted",
    "Succeeded",
]


def test_metadata(cromwell_api, submit_wdls):
    """Getting workflow metadata works"""
    params = {"expandSubWorkflows": False, "excludeKey": "calls"}
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api.metadata(x, params=params)
        assert isinstance(res, dict)

        if res["status"] in states_not_final:
            assert list(res.keys()) == meta_keys_state_submitted
        elif res["status"] in states_final:
            assert list(res.keys()) == meta_keys_state_final
        else:
            pass
