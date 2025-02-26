import os
from io import StringIO
from pathlib import Path

import sh
from colorama import Fore, Style, init

init(autoreset=True)


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

    def validate(self, wdl_path, show_cmd=False):
        try:
            self.womtool = self.womtool.bake(
                "validate",
                f"{wdl_path}/{wdl_path}.wdl",
            )
            self.has_inputs(wdl_path)
            if show_cmd:
                print(self.womtool)
            self.womtool()
        except sh.ErrorReturnCode as e:
            print(f"Command {e.full_cmd} exited with {e.exit_code}")
            return False

        return True


class CromwellJava(object):
    """Cromwell Java class - run Cromwell Java jar"""

    def __init__(self):
        self.stderr = StringIO()
        self.stdout = StringIO()
        self.cromwell_path = os.getenv("CROMWELL_PATH")
        if not self.cromwell_path:
            raise Exception("failed setting CROMWELL_PATH")
        self.cromwell = sh.Command("java").bake("-jar", "-Dconfig.file=cromwell.conf", self.cromwell_path)

    def has_inputs(self, wdl_path):
        path = Path(f"{wdl_path}/inputs.json")
        if path.exists():
            self.cromwell = self.cromwell.bake(i=str(path))

    def has_options(self, wdl_path):
        path = Path(f"{wdl_path}/options.json")
        if path.exists():
            self.cromwell = self.cromwell.bake(o=str(path))

    def run(self, wdl_path, show_cmd=False):
        try:
            self.cromwell = self.cromwell.bake(
                "run",
                f"{wdl_path}/{wdl_path}.wdl",
            )
            self.has_inputs(wdl_path)
            self.has_options(wdl_path)
            if show_cmd:
                print(self.cromwell)
            self.cromwell(_out=self.stdout, _err=self.stderr)
        except sh.ErrorReturnCode as e:
            print(
                Fore.RED
                + Style.BRIGHT
                + f"\nCommand {e.full_cmd} exited with {e.exit_code}\n"
            )
            print(Fore.RED + Style.BRIGHT + f"Dumping cromwell run output\n")
            print(Fore.YELLOW + Style.BRIGHT + "STDERR output:\n")
            print(self.stderr.getvalue())
            print(Fore.YELLOW + Style.BRIGHT + "STDOUT output:\n")
            print(self.stdout.getvalue())
            return False

        return True
