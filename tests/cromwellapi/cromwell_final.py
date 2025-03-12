import time

from cromwell import CromwellApi
from utils import workflow_states


class CromwellApiFinal(CromwellApi):
    """
    CromwellApiFinal

    Wrapper for `CromwellApi` methods that are run in the background
    on a Cromwell server, and have initial and final states. These
    methods are the named the same as those in `CromwellApi` but
    internally run the `CromwellApi` method in a `while` loop until
    the response has a final state (aborted, failed, succeeded).

    Examples:
        # in the root of the repo
        import sys
        sys.path.append('tests/cromwellapi/')

        from pathlib import Path
        from proof import ProofApi
        from cromwell import CromwellApi
        from utils import path_wdl

        proof_api = ProofApi()
        cromwell_url = proof_api.cromwell_url()
        cromwell_api = CromwellApi(url=cromwell_url)
        wdl_path = path_wdl("helloHostname")
        res = cromwell_api.submit_workflow(wdl_path=wdl_path)
        con = CromwellApiFinal(url=cromwell_url, recording_mode="once", sleep=5)
        params = {"expandSubWorkflows": True}
        con.metadata(workflow_id=res["id"], params=params)
    """

    def __init__(self, url, recording_mode, sleep):
        super().__init__(url)
        # self.logger = logging.getLogger(__name__)
        self.mode = recording_mode
        self.sleep_sec = sleep if self.mode == "rewrite" else 0
        self.workflow_states = workflow_states

    def until_final(self, method, **kwargs):
        """until final: call a CromwellApi method until it returns a final state"""
        super_method = getattr(super(), method)
        not_final = True
        while not_final:
            # self.logger.info(f"Sleeping {self.sleep_sec} seconds\n")
            time.sleep(self.sleep_sec)
            res = super_method(**kwargs)
            if res.get("status") is not None:
                not_final = res.get("status").lower() not in [
                    x.lower() for x in self.workflow_states["final"]
                ]

        return res

    def metadata(self, workflow_id, params):
        """metadata: call CromwellApi.metadata until returns a final state"""
        return self.until_final(
            "metadata", workflow_id=workflow_id, params=params
        )
