import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .constants import TOKEN
from .utils import (
    before_sleep_message,
    find_project_root,
    past_date,
    token_check,
)


def as_file_object(path=None):
    if not path:
        return None
    return open(path, mode="rb")


def path_as_string(x):
    if not x:
        return None
    return str(x.absolute())


class CromwellApi(object):
    """CromwellApi class"""

    def __init__(self, url):
        self.base_url = url.rstrip("/")
        self.token = token_check(TOKEN)
        self.headers = {"Authorization": f"Bearer {TOKEN}"}

    def submit_workflow(
        self,
        wdl_path,
        inputs=None,
        labels=None,
        options=None,
    ):
        files = {
            "workflowSource": as_file_object(path_as_string(wdl_path)),
            "workflowInputs": as_file_object(path_as_string(inputs)),
            "labels": as_file_object(path_as_string(labels)),
            "workflowOptions": as_file_object(path_as_string(options)),
        }
        files = {k: v for k, v in files.items() if v}
        res = httpx.post(
            f"{self.base_url}/api/workflows/v1",
            headers=self.headers,
            files=files,
        )
        res.raise_for_status()
        data = res.json()
        data["path"] = str(wdl_path.relative_to(find_project_root()))
        return data

    @retry(
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_message,
    )
    def metadata(self, workflow_id, params={}):
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

    def validate(self, wdl_path, inputs=None, options=None):
        files = {
            "workflowSource": as_file_object(path_as_string(wdl_path)),
            "workflowInputs": as_file_object(path_as_string(inputs)),
            "workflowOptions": as_file_object(path_as_string(options)),
        }
        files = {k: v for k, v in files.items() if v}
        res = httpx.post(
            f"{self.base_url}/api/womtool/v1/describe",
            headers=self.headers,
            files=files,
        )
        res.raise_for_status()
        return res.json()

    def abort(self, workflow_id):
        res = httpx.post(
            f"{self.base_url}/api/workflows/v1/{workflow_id}/abort",
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json()

    def search(self, days=1, name=None, status=None):
        submission = f"{past_date(days)}T00:00Z"
        params = {"submission": submission, "name": name, "status": status}
        params = {k: v for k, v in params.items() if v}
        res = httpx.get(
            f"{self.base_url}/api/workflows/v1/query",
            headers=self.headers,
            params=params,
        )
        res.raise_for_status()
        return res.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_message,
    )
    def outputs(self, workflow_id):
        res = httpx.get(
            f"{self.base_url}/api/workflows/v1/{workflow_id}/outputs",
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json()

    @retry(
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before_sleep=before_sleep_message,
    )
    def labels(self, workflow_id):
        res = httpx.get(
            f"{self.base_url}/api/workflows/v1/{workflow_id}/labels",
            headers=self.headers,
        )
        res.raise_for_status()
        return res.json()
