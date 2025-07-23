import httpx
from tenacity import (
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .constants import PROOF_BASE_URL, REGULATED_DATA, SLURM_ACCOUNT, TOKEN
from .utils import before_sleep_message, token_check


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

    def __init__(self, slurm_account: str = "", regulated_data: bool = False):
        self.base_url = PROOF_BASE_URL
        self.token = token_check(TOKEN)
        self.headers = {"Authorization": f"Bearer {TOKEN}"}
        self.slurm_account = SLURM_ACCOUNT if SLURM_ACCOUNT else slurm_account
        self.regulated_data = bool(
            REGULATED_DATA if REGULATED_DATA else regulated_data
        )

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
        retry=retry_if_exception(
            lambda e: (
                isinstance(e, httpx.ReadTimeout)
                or (
                    isinstance(e, httpx.HTTPStatusError)
                    and e.response.status_code != 409
                )
            )
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
            json={
                "slurm_account": self.slurm_account,
                "regulated_data": self.regulated_data,
            },
        )
        if res.status_code != 409:
            res.raise_for_status()

        return res

    @retry(
        retry=retry_if_exception(
            lambda e: (
                isinstance(e, httpx.ReadTimeout)
                or (
                    isinstance(e, httpx.HTTPStatusError)
                    and e.response.status_code != 409
                )
            )
        ),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_message,
    )
    def stop(self, timeout=25):
        res = httpx.delete(
            f"{self.base_url}/cromwell-server",
            headers=self.headers,
            timeout=timeout,
        )
        res.raise_for_status()
        return res

    def start_if_not_up(self):
        if not self.is_cromwell_server_up():
            return self.start()

    def wait_for_stopped(self):
        import time

        print("waiting for cromwell server to stop ...")
        ready_to_start = False
        while not ready_to_start:
            canJobStart = self.is_cromwell_server_up()
            if not canJobStart:
                ready_to_start = True
            else:
                time.sleep(1)

    def wait_for_up(self):
        import time

        print("waiting for cromwell server to be up ...")
        has_cromwell_url = False
        while not has_cromwell_url:
            the_url = self.status()["cromwellUrl"]
            if the_url:
                has_cromwell_url = True
            else:
                time.sleep(1)

    def cromwell_url(self):
        # self.start_if_not_up()
        status = self.status()
        if status["canJobStart"]:
            # server off; can start both reg and non-reg
            self.start()
        elif (
            # non-reg server on; stop and start up reg server
            not self.regulated_data and status["jobInfo"]["USE_REGULATED_DATA"]
        ) | (
            # reg server on; stop and start up non-reg server
            self.regulated_data and not status["jobInfo"]["USE_REGULATED_DATA"]
        ):
            mssg = "supporting regulated data"
            print(
                f"""
                Asking for regulated data: {self.regulated_data}
                Cromwell server on and {f"not {mssg}" if status["jobInfo"]["USE_REGULATED_DATA"] else mssg}
                Restarting server
                """
            )
            self.stop()
            self.wait_for_stopped()
            self.start()
            self.wait_for_up()
            status = self.status()
        return status["cromwellUrl"]
