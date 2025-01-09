import json
from pathlib import Path

import pytest
from mocks import MockProofApi

from cromwell import CromwellApi
from proof import ProofApi

mocked_submissions = "tests/cromwellapi/mocked_submissions.json"


@pytest.fixture(scope="session")
def cromwell_api(request):
    recording_mode = request.config.getoption("--record-mode", default=None)

    if recording_mode != "rewrite":
        proof_api = MockProofApi()
    else:
        proof_api = ProofApi()

    cromwell_url = proof_api.cromwell_url()

    return CromwellApi(url=cromwell_url)


@pytest.fixture(scope="session")
def submit_wdls(request, cromwell_api):
    """
    This fixture runs automatically before any tests.
    Uses "session" scope to run only once for all tests.
    """
    recording_mode = request.config.getoption("--record-mode", default=None)

    root = Path(__file__).parents[2].resolve()
    pattern = "**/*.wdl"
    wdl_paths = list(root.glob(pattern))

    if recording_mode == "rewrite":
        print(f"\nSubmitting {len(wdl_paths)} wdls ...")
        out = [cromwell_api.submit_workflow(wdl_path=path) for path in wdl_paths]
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
    return {"filter_headers": ["authorization"]}
