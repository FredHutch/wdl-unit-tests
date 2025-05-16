import os
import re

import pytest

from .constants import SLEEP_FINAL_STATE
from .cromwell import CromwellApi
from .cromwell_final import CromwellApiFinal
from .mocks import MockProofApi
from .proof import ProofApi
from .utils_cassettes import cassettes_last_modified


def pytest_report_header(config):
    mode = config.getoption("--record-mode", default=None)
    last_mod = cassettes_last_modified("tests/cromwellapi/cassettes")
    retry_messages_warn = (
        "" if mode == "rewrite" else "(ignore Retry attempt messages)"
    )
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


@pytest.fixture
def test_name(request):
    return request.node.name


def add_cassette_path(path):
    """
    Examples:
      add_cassette_path("tests/cromwellapi/test-call.py::test_call_final[globNonmatching.wdl]")
      #> 'tests/cromwellapi/cassettes/test-call/test_call_final[globNonmatching.wdl].yaml'
    """
    path = path.replace(".py::", "/")
    path = path.replace("tests/cromwellapi", "tests/cromwellapi/cassettes")
    path = path + ".yaml"
    return path


def add_mock_json_path(path):
    """
    Examples:
      add_mock_json_path("tests/cromwellapi/test-call.py::test_call_final[globNonmatching.wdl]")
      #> 'tests/cromwellapi/mocked_submissions/test_call_final[globNonmatching.wdl].json'
    """
    path = re.sub("test-.+.py::", "", path)
    path = path.replace(
        "tests/cromwellapi", "tests/cromwellapi/mocked_submissions"
    )
    path = path + ".json"
    return path


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report):
    for test_data in json_report["tests"]:
        test_data["cassette"] = add_cassette_path(test_data["nodeid"])
        test_data["mock_json"] = add_mock_json_path(test_data["nodeid"])
