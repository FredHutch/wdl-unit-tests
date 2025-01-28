from datetime import datetime, timedelta
from pathlib import Path

metadata_response_keys = {
    "running": [
        "workflowName",
        "workflowProcessingEvents",
        "actualWorkflowLanguageVersion",
        "submittedFiles",
        "calls",
        "outputs",
        "workflowRoot",
        "actualWorkflowLanguage",
        "status",
        "start",
        "id",
        "inputs",
        "labels",
        "submission",
    ],
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
    "aborted": [
        "submittedFiles",
        "calls",
        "outputs",
        "status",
        "id",
        "inputs",
        "labels",
        "submission",
    ],
    "failed": [
        "workflowProcessingEvents",
        "actualWorkflowLanguageVersion",
        "submittedFiles",
        "calls",
        "outputs",
        "actualWorkflowLanguage",
        "status",
        "failures",
        "end",
        "start",
        "id",
        "inputs",
        "labels",
        "submission",
    ],
    "succeeded": [
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


def path_wdl(wdl):
    path = Path(__file__).parents[2].resolve()
    return path / f"{wdl}/{wdl}.wdl"


def path_options(wdl):
    path = Path(__file__).parents[2].resolve()
    return path / f"{wdl}/options.json"


def path_inputs(wdl):
    path = Path(__file__).parents[2].resolve()
    return path / f"{wdl}/inputs.json"


def past_date(days):
    now = datetime.now()
    past_date = now - timedelta(days=days)
    return past_date.strftime("%Y-%m-%d")
