import os
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


class MissingProofToken(Exception):
    pass


def token_check(token):
    if token is None:
        raise MissingProofToken("Couldn't access env var PROOF_API_TOKEN_DEV")
    return token


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


def before_sleep_message(state):
    print(
        f"Retrying in {state.next_action.sleep} seconds, attempt {state.attempt_number}"
    )


def fetch_wdl_paths():
    root = Path(__file__).parents[2].resolve()
    return list(root.glob("**/*.wdl"))


def find_project_root(marker_file="pyproject.toml"):
    """
    A hack to avoid using __file__ as that does not work when using a
    python repl (python or ipython)
    """
    current_dir = os.getcwd()

    while True:
        if os.path.exists(os.path.join(current_dir, marker_file)):
            return current_dir

        parent_dir = os.path.dirname(current_dir)

        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    return current_dir
