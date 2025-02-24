from pathlib import Path
from urllib.parse import urlparse, urlunparse

import yaml


class MockProofApi(object):
    """Mock ProofApi class"""

    def cromwell_url(self):
        path = Path(
            "tests", "cromwellapi", "cassettes", "test-outputs", "test_outputs.yaml"
        )
        path_full = path.resolve()
        with open(str(path_full), "r") as file:
            data = yaml.safe_load(file)
        uri = data["interactions"][0]["request"]["uri"]
        urip = urlparse(uri)
        return f"{urip.scheme}://{urip.netloc}/"
