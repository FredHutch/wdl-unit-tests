import json
from pathlib import Path

import pytest

from mocks import MockProofApi
from utils_cassettes import cassettes_last_modified
from cromwell import CromwellApi
from proof import ProofApi

mocked_submissions = "tests/cromwellapi/mocked_submissions.json"


def pytest_report_header(config):
    mode = config.getoption("--record-mode", default=None)
    last_mod = cassettes_last_modified("tests/cromwellapi/cassettes")
    retry_messages_warn = (
        "" if recording_mode == "rewrite" else "(ignore Retry attempt messages)"
    )
    return [
        f"vcr recording mode: {mode} {retry_messages_warn}",
        f"vcr cassettes last recorded approx.: {last_mod}",
    ]


@pytest.fixture(scope="session")
def recording_mode(request):
    return request.config.getoption("--record-mode", default=None)


@pytest.fixture(scope="session")
def cromwell_api(recording_mode):
    if recording_mode != "rewrite":
        proof_api = MockProofApi()
    else:
        proof_api = ProofApi()

    cromwell_url = proof_api.cromwell_url()

    return CromwellApi(url=cromwell_url)


@pytest.fixture(scope="session")
def submit_wdls(recording_mode, cromwell_api):
    """
    This fixture runs automatically before any tests.
    Uses "session" scope to run only once for all tests.
    """
    root = Path(__file__).parents[2].resolve()
    pattern = "**/*.wdl"
    wdl_paths = list(root.glob(pattern))

    if recording_mode == "rewrite":
        print(f"\nSubmitting {len(wdl_paths)} wdls ...")
        out = []
        for path in wdl_paths:
            opts_path = path.parent / "options.json"
            opts_path = opts_path if opts_path.exists() else None
            res = cromwell_api.submit_workflow(wdl_path=path, options=opts_path)
            out.append(res)
        with open(mocked_submissions, "w") as f:
            json.dump(out, f, indent=4)
    else:
        with open(mocked_submissions, "r") as f:
            out = json.load(f)

    # Yield to let tests run
    yield out

    # Cleanup is not possible for Cromwell - but would be here


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # completely removes Authorization header from all http requests
        "filter_headers": ["authorization"],
        # matches only on HTTP method, scheme (http/https), path (a/b/c), and query (?a=5)
        # does not match on host (gizmoxxx.fhcrcc.org:<port>) b/c that can change
        "match_on": ["method", "scheme", "path", "query"],
    }
