import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from utils import PROOF_BASE_URL, TOKEN, token_check, before_sleep_message


class ProofApi(object):
    """ProofApi class"""

    def __init__(self):
        self.base_url = PROOF_BASE_URL
        self.token = token_check(TOKEN)
        self.headers = {"Authorization": f"Bearer {TOKEN}"}

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.ReadTimeout)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_message,
    )
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

    @retry(
        retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.ReadTimeout)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_message,
    )
    def start(self, timeout=10):
        return httpx.post(
            f"{self.base_url}/cromwell-server",
            headers=self.headers,
            timeout=timeout,
            json={"slurm_account": None},
        )

    def start_if_not_up(self):
        if not self.is_cromwell_server_up():
            return self.start()

    def cromwell_url(self):
        self.start_if_not_up()
        return self.status()["cromwellUrl"]
