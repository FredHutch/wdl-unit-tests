from pathlib import Path

import pytest

from cromwell import CromwellApi
from proof import ProofApi

proof_api = ProofApi()
cromwell_url = proof_api.cromwell_url()


@pytest.fixture(scope="session")
def cromwell_api():
    return CromwellApi(url=cromwell_url)


@pytest.fixture(scope="session")
def submit_wdls(cromwell_api):
    """
    This fixture runs automatically before any tests.
    Uses "session" scope to run only once for all tests.
    """
    root = Path(__file__).parents[2].resolve()
    pattern = "**/*.wdl"
    wdl_paths = list(root.glob(pattern))

    print(f"Submitting {len(wdl_paths)} wdls ...")

    out = []
    for path in wdl_paths:
        opts_path = path.parent / "options.json"
        opts_path = opts_path if opts_path.exists() else None
        res = cromwell_api.submit_workflow(wdl_path=path, options=opts_path)
        out.append(res)

    # Yield to let tests run
    yield out

    # Cleanup is not possible for Cromwell - but would be here
