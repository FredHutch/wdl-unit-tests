import json
from pathlib import Path

BASE_TESTS_PATH = "tests/cromwellapi"


def add_mocked_submission(res, test_name):
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
    mocked_subs = Path(
        f"{BASE_TESTS_PATH}/mocked_submissions/{test_name}.json"
    ).resolve()

    wdl_path = str(path.relative_to(Path.cwd()))
    with open(mocked_subs, "r") as f:
        subs = json.load(f)

    return [d for d in subs if d["path"] == wdl_path][0]


def submit_wdl(path, recording_mode, cromwell_api, test_name):
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
