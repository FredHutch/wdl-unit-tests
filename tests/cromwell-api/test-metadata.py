workflow_meta_keys = [
    "submittedFiles",
    "calls",
    "outputs",
    "status",
    "id",
    "inputs",
    "labels",
    "submission",
]


def test_metadata(cromwell_api, submit_wdls):
    """Getting workflow metadata works"""
    ids = [wf["id"] for wf in submit_wdls]
    for x in ids:
        res = cromwell_api.metadata(x)
        assert isinstance(res, dict)
        # assert list(res.keys()) == workflow_meta_keys
