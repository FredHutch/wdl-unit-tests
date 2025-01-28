import httpx

from constants import PROOF_BASE_URL, TOKEN


class ProofApi(object):
    """ProofApi class"""

    def __init__(self):
        self.base_url = PROOF_BASE_URL
        self.token = TOKEN
        self.headers = {"Authorization": f"Bearer {TOKEN}"}

    def status(self, timeout=10):
        res = httpx.get(
            f"{self.base_url}/cromwell-server",
            headers=self.headers,
            timeout=timeout,
        )
        res.raise_for_status()
        return res.json()

    def is_cromwell_server_up(self, timeout=10):
        return not self.status()["canJobStart"]

    def start(self):
        res = httpx.post(
            f"{self.base_url}/cromwell-server",
            headers=self.headers,
            json={"slurm_account": None},
        )
        res.raise_for_status()
        return res

    def start_if_not_up(self):
        if not self.is_cromwell_server_up():
            return self.start()

    def cromwell_url(self):
        self.start_if_not_up()
        return self.status()["cromwellUrl"]
