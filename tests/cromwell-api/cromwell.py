import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from utils import TOKEN


def as_file_object(path=None):
    if not path:
        return None
    return open(path, mode="rb")


def my_before_sleep(state):
    print(
        f"Retrying in {state.next_action.sleep} seconds, attempt {state.attempt_number}"
    )


class CromwellApi(object):
    """CromwellApi class"""

    def __init__(self, url):
        self.base_url = url.rstrip("/")
        self.token = TOKEN
        self.headers = {"Authorization": f"Bearer {TOKEN}"}

    def submit_workflow(
        self,
        wdl_path,
        batch=None,
        params=None,
    ):
        files = {
            "workflowSource": as_file_object(str(wdl_path.absolute())),
            "workflowInputs": as_file_object(batch),
            "workflowInputs_2": as_file_object(params),
        }
        files = {k: v for k, v in files.items() if v}
        res = httpx.post(
            f"{self.base_url}/api/workflows/v1", headers=self.headers, files=files
        )
        res.raise_for_status()
        return res.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=my_before_sleep,
    )
    def metadata(self, workflow_id):
        params = {"expandSubWorkflows": False, "excludeKey": "calls"}
        res = httpx.get(
            f"{self.base_url}/api/workflows/v1/{workflow_id}/metadata",
            headers=self.headers,
            params=params,
        )
        res.raise_for_status()
        return res.json()

    def version(self):
        res = httpx.get(
            f"{self.base_url}/engine/v1/version",
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json()
