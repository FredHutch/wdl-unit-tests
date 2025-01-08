import os
from datetime import datetime, timedelta
from pathlib import Path

PROOF_BASE_URL = "https://proof-api-dev.fredhutch.org"
TOKEN = os.getenv("PROOF_API_TOKEN_DEV")

metadata_response_keys = {
    "submitted": [
        "submittedFiles",
        "calls",
        "outputs",
        "status",
        "id",
        "inputs",
        "labels",
        "submission",
    ],
    "final": [
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
    ],
}

workflow_states = {
    "not_final": [
        "Running",
        "Submitted",
        "Pending",
    ],
    "final": [
        "Failed",
        "Aborted",
        "Succeeded",
    ],
}


def make_path(file):
    path = Path(__file__).parents[2].resolve()
    return path / f"{file}/{file}.wdl"


def past_date(days):
    now = datetime.now()
    past_date = now - timedelta(days=days)
    return past_date.strftime("%Y-%m-%d")
