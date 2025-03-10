from pathlib import Path
from unittest.mock import patch

import pytest
from utils import path_options, path_wdl

LABELS_FILE_1 = Path("tests/cromwellapi/labels1.json")


@pytest.mark.vcr
def test_labels(cromwell_api, recording_mode):
    """Getting workflow labels works"""
    job = cromwell_api.submit_workflow(
        wdl_path=path_wdl("helloHostname"),
        labels=LABELS_FILE_1,
        options=path_options("helloHostname"),
    )
    if recording_mode != "rewrite":
        with patch("time.sleep"):
            res = cromwell_api.labels(workflow_id=job["id"])
    else:
        res = cromwell_api.labels(workflow_id=job["id"])

    assert isinstance(res, dict)
