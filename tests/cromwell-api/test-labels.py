from pathlib import Path

from utils import make_path

LABELS_FILE_1 = Path("tests/cromwell-api/labels1.json")

def test_labels(cromwell_api):
    """Getting workflow labels works"""
    job = cromwell_api.submit_workflow(
        wdl_path=make_path("helloHostname"), labels=LABELS_FILE_1
    )
    res = cromwell_api.labels(workflow_id=job["id"])
    assert isinstance(res, dict)
