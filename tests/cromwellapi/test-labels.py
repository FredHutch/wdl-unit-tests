import pytest
from pathlib import Path

from utils import path_wdl, path_options

LABELS_FILE_1 = Path("tests/cromwellapi/labels1.json")


@pytest.mark.vcr
def test_labels(cromwell_api):
    """Getting workflow labels works"""
    job = cromwell_api.submit_workflow(
        wdl_path=path_wdl("helloHostname"),
        labels=LABELS_FILE_1,
        options=path_options("helloHostname"),
    )
    res = cromwell_api.labels(workflow_id=job["id"])
    assert isinstance(res, dict)
