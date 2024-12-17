import re
import time
from pathlib import Path

from cromwell import CromwellApi
from proof import ProofApi


def make_path(file):
    path = Path(__file__).parents[2].resolve()
    return path / f"{file}/{file}.wdl"


proof_api = ProofApi()
# proof_api.status()
# proof_api.is_cromwell_server_up()
cromwell_url = proof_api.cromwell_url()
cromwell_api = CromwellApi(url=cromwell_url)

# cromwell_api.submit_workflow(wdl_path=make_path("helloHostname"))
# cromwell_api.submit_workflow(
#     wdl_path=Path("../../helloHostname/helloHostname.wdl").resolve()
# )
# cromwell_api.metadata('f8c84698-164e-4b5d-b64e-81256209949c')


def test_submit_works():
    """Submitting a WDL file works"""
    submit_res = cromwell_api.submit_workflow(wdl_path=make_path("helloHostname"))
    time.sleep(5)
    metadata_submitted = cromwell_api.metadata(submit_res["id"])
    print(metadata_submitted)
    assert isinstance(submit_res, dict)
    assert isinstance(metadata_submitted, dict)
    assert submit_res["status"] == "Submitted"
    assert metadata_submitted["status"] == "Submitted"
    assert (
        re.search("HelloHostname", metadata_submitted["submittedFiles"]["workflow"])
        is not None
    )
