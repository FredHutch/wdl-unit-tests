import os
import re

import pytest


@pytest.mark.vcr
def test_regulated_paths(proof_api):
    """
    Test the Cromwell version endpoint (/engine/v1/version)

    We're not testing exact version number as we just care about the data type

    Args:
        cromwell_api (CromwellApi): Cromwell server being used to submit WDL unit tests (class defined in cromwell.py)
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
