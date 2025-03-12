import httpx
from constants import PROOF_BASE_URL, TOKEN
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from utils import before_sleep_message, token_check


def cache_next_call_only(func):
    """Cache the next call only

    Examples:
        import time

        @cache_next_call_only
        def expensive_function(x):
            return time.sleep(x)

        expensive_function(5)  # Expensive computation performed
        expensive_function(5)  # Cached result returned
        expensive_function(5)  # Expensive computation performed again
    """
    cache = {}

    def wrapper(*args, **kwargs):
        if "result" in cache:
            print("result in cache, returning it")
            result = cache.pop("result")
            return result
        else:
            print("result not in cache")
            result = func(*args, **kwargs)
            cache["result"] = result
            return result

    return wrapper


class ProofApi(object):
    """ProofApi class"""

    def __init__(self):
        self.base_url = PROOF_BASE_URL
        self.token = token_check(TOKEN)
        self.headers = {"Authorization": f"Bearer {TOKEN}"}

    @cache_next_call_only
    @retry(
        retry=retry_if_exception_type(
            (httpx.HTTPStatusError, httpx.ReadTimeout)
        ),
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
        return not self.status(timeout=timeout)["canJobStart"]

    @retry(
        retry=retry_if_exception_type(
            (httpx.HTTPStatusError, httpx.ReadTimeout)
        ),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_message,
    )
    def start(self, timeout=10):
        res = httpx.post(
            f"{self.base_url}/cromwell-server",
            headers=self.headers,
            timeout=timeout,
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
