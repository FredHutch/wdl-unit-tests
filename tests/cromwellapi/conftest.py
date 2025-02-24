import json
import os
from pathlib import Path

import pytest
from constants import SLEEP_FINAL_STATE
from cromwell import CromwellApi
from cromwell_final import CromwellApiFinal
from mocks import MockProofApi
from proof import ProofApi
from utils_cassettes import cassettes_last_modified

mocked_submissions = "tests/cromwellapi/mocked_submissions.json"


def pytest_report_header(config):
    mode = config.getoption("--record-mode", default=None)
    last_mod = cassettes_last_modified("tests/cromwellapi/cassettes")
    retry_messages_warn = "" if mode == "rewrite" else "(ignore Retry attempt messages)"
    return [
        f"vcr recording mode: {mode} {retry_messages_warn}",
        f"vcr cassettes last recorded approx.: {last_mod}",
    ]


@pytest.fixture(scope="session")
def recording_mode(request):
    return request.config.getoption("--record-mode", default=None)


@pytest.fixture(scope="session")
def proof_api(recording_mode):
    if recording_mode != "rewrite":
        return MockProofApi()
    else:
        return ProofApi()


@pytest.fixture(scope="session")
def cromwell_api(proof_api):
    cromwell_url = proof_api.cromwell_url()

    return CromwellApi(url=cromwell_url)


@pytest.fixture(scope="session")
def cromwell_api_final(proof_api, recording_mode):
    cromwell_url = proof_api.cromwell_url()

    return CromwellApiFinal(
        url=cromwell_url, recording_mode=recording_mode, sleep=SLEEP_FINAL_STATE
    )


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


class EnvironmentVariableError(Exception):
    """Custom error class for a missing environment variable"""

    pass


def filter_response_bodies(response):
    """Filter sensitive things out of vcr response bodies

    Used only for file paths for now, but could be modified
    to accept other things to hide
    """
    # PATH_ROOTS env var is set in the github repo under actions secrets
    path_roots = os.getenv("PATH_ROOTS")

    if not path_roots:
        raise EnvironmentVariableError("could not find PATH_ROOTS env var")

    paths = path_roots.split(",")

    response["body"]["string"] = response["body"]["string"].decode("utf-8")
    for path in paths:
        response["body"]["string"] = response["body"]["string"].replace(
            path, "/redacted"
        )

    response["body"]["string"] = response["body"]["string"].encode("utf-8")

    return response


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # this decodes gzip/deflate content type responses as human readable text
        "decode_compressed_response": True,
        # completely removes Authorization header from all http requests
        "filter_headers": ["authorization"],
        # matches only on HTTP method, scheme (http/https), path (a/b/c), and query (?a=5)
        # does not match on host (gizmoxxx.fhcrcc.org:<port>) b/c that can change
        "match_on": ["method", "scheme", "path", "query"],
        # remove parts of paths that start with PATH_ROOTS
        "before_record_response": filter_response_bodies,
    }
