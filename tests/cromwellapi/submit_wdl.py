import json
from pathlib import Path

BASE_TESTS_PATH = "tests/cromwellapi"


def add_mocked_submission(res, test_name):
    """Add a mocked submission file to disk. This function is used when
    `recording_mode` is set to "rewrite" (meaning make a real request to
    submit a WDL).

    Args:
        res (dict): Response from a job submission against the Cromwell API.
          dict has keys: "id", "status", "path"
        test_name (str): name of the test being run

    Returns:
        None
    """
    mocked_subs = Path(
        f"{BASE_TESTS_PATH}/mocked_submissions/{test_name}.json"
    ).resolve()

    if mocked_subs.exists():
        with open(mocked_subs, "r") as f:
            subs = json.load(f)

        subs = [res if x["path"] == res["path"] else x for x in subs]
    else:
        subs = []
        subs.append(res)

    with open(mocked_subs, "w") as f:
        json.dump(subs, f, indent=4)


def use_mocked_submission(path, test_name):
    """Use a mocked WDL job submission file from disk.
    This function is used when `recording_mode` is not set to "rewrite"
    (e.g., "once" - meaning use mock file and cached vcr cassettes).

    Args:
        path (Path): Path to the WDL file
        test_name (str): name of the test being run

    Returns:
      dict: Submission result with keys: "id", "status", "path"
    """
    mocked_subs = Path(
        f"{BASE_TESTS_PATH}/mocked_submissions/{test_name}.json"
    ).resolve()

    wdl_path = str(path.relative_to(Path.cwd()))
    with open(mocked_subs, "r") as f:
        subs = json.load(f)

    return [d for d in subs if d["path"] == wdl_path][0]


def submit_wdl(path, recording_mode, cromwell_api, test_name):
    """Submit a WDL workflow to the Cromwell API

    Args:
        path (Path): Path to the WDL file
        recording_mode (str): string indicating if the cassettes are getting rewritten or not, fixture defined in conftest.py
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
        test_name (str): name of the test being run

    Returns:
        dict: Submission result with keys: "id", "status", "path"
    """
    if recording_mode == "rewrite":
        inputs_path = path.parent / "inputs.json"
        inputs_path = inputs_path if inputs_path.exists() else None
        opts_path = path.parent / "options.json"
        opts_path = opts_path if opts_path.exists() else None
        res = cromwell_api.submit_workflow(
            wdl_path=path, inputs=inputs_path, options=opts_path
        )
        add_mocked_submission(res, test_name)
    else:
        res = use_mocked_submission(path, test_name)

    return res
