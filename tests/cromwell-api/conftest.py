import pytest
from cromwell import CromwellApi
from proof import ProofApi

proof_api = ProofApi()
cromwell_url = proof_api.cromwell_url()


@pytest.fixture
def cromwell_api():
    return CromwellApi(url=cromwell_url)
