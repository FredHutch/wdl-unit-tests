from pathlib import Path

import pytest
from cromwell import CromwellApi
from proof import ProofApi

proof_api = ProofApi()
cromwell_url = proof_api.cromwell_url()


@pytest.fixture(scope="session")
def cromwell_api():
    return CromwellApi(url=cromwell_url)


@pytest.fixture(scope="session", autouse=True)
def submit_wdls(cromwell_api):
    """
    This fixture runs automatically before any tests.
    Uses "session" scope to run only once for all tests.
    """
    root = Path(__file__).parents[2].resolve()
    pattern = "**/*.wdl"
    wdl_paths = list(root.glob(pattern))

    print(f"Submitting {len(wdl_paths)} wdls ...")

    out = [cromwell_api.submit_workflow(wdl_path=path) for path in wdl_paths]

    # Yield to let tests run
    yield out

    # Cleanup is not possible for Cromwell - but would be here
