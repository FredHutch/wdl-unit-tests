import os
from pathlib import Path

import sh


class Womtool(object):
    """Womtool class"""

    def __init__(self):
        self.womtool_path = os.getenv("WOMTOOL_PATH")
        if not self.womtool_path:
            raise Exception("failed setting WOMTOOL_PATH")
        self.womtool = sh.Command("java").bake("-jar", self.womtool_path)

    def has_inputs(self, wdl_path):
        path = Path(f"{wdl_path}/inputs.json")
        if path.exists():
            self.womtool = self.womtool.bake(i=str(path))

    def validate(self, wdl_path, verbose=False):
        try:
            self.has_inputs(wdl_path)
            self.womtool = self.womtool.bake(
                "validate",
                f"{wdl_path}/{wdl_path}.wdl",
            )
            if verbose:
                print(self.womtool)
            self.womtool()
        except sh.ErrorReturnCode as e:
            print(f"Command {e.full_cmd} exited with {e.exit_code}")
            return False

        return True
