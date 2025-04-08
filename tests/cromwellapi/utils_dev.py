import sys
from functools import lru_cache
from pathlib import Path

from cromwell import CromwellApi
from proof import ProofApi
from utils import find_project_root


@lru_cache(maxsize=None)
def capi():
    """Create a CromwellApi instance using the ProofApi

    Cached so that we don't have to connect w/ ProofApi again
    """
    proof_api = ProofApi()
    cromwell_url = proof_api.cromwell_url()
    return CromwellApi(url=cromwell_url)


def submit_workflow(wdl_name):
    """Submit a workflow to Cromwell

    Args:
        wdl_name (str): The folder name of the workflow to submit

    Examples:
      from utils_dev import submit_workflow
      submit_workflow("helloHostname")
      # can also run from cli like this:
      # op run -- uv run tests/cromwellapi/utils_dev.py emptyGlobTest
    """
    base = find_project_root()
    wdl_path = Path(f"{str(base)}/{wdl_name}/{wdl_name}.wdl")
    inputs_path = wdl_path.parent / "inputs.json"
    inputs_path = inputs_path if inputs_path.exists() else None
    opts_path = wdl_path.parent / "options.json"
    opts_path = opts_path if opts_path.exists() else None
    cromwell_api = capi()
    res = cromwell_api.submit_workflow(
        wdl_path=wdl_path, inputs=inputs_path, options=opts_path
    )
    return res


if __name__ == "__main__":
    x = str(sys.argv[1])
    print(submit_workflow(x))
