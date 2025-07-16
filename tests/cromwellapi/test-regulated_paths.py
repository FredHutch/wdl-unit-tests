import os
import re

import pytest


@pytest.mark.vcr
def test_regulated_paths(proof_api):
    """
    Test that the scratch directory is within the regulated data path
    when using a regulated data Cromwell server

    Args:
        proof_api (ProofApi): ProofApi instance from proof.py
    """
    if not hasattr(proof_api, "regulated_data"):
        pytest.skip("Regulated data not enabled")

    if not proof_api.regulated_data:
        pytest.skip("Regulated data not enabled")

    path_roots = os.getenv("PATH_ROOTS")

    if not path_roots:
        pytest.skip("PATH_ROOTS not set")

    prefix = list(
        filter(None, [re.search(".+ula.+", w) for w in path_roots.split(",")])
    )[0].string

    status = proof_api.status()
    assert status["jobInfo"]["SCRATCHDIR"].startswith(prefix)
