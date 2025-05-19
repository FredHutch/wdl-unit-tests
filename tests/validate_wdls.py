import logging

from cromwellapi.utils import fetch_wdl_paths
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler(show_time=False)],
)
log = logging.getLogger("rich")


def validate_wdls(wdl_paths):
    [check_wdl_name_matches(w) for w in wdl_paths]
    [check_for_other_json_files(w) for w in wdl_paths]


def check_wdl_name_matches(path):
    if not path.name.replace(".wdl", "") == path.parent.name:
        log.warning(
            f"WDL file name {path.name} and dir name {path.parent.name} do not match"
        )


def check_for_other_json_files(path):
    jsons = list(path.parent.glob("*.json"))
    if jsons:
        for json in jsons:
            if json.name not in ["options.json", "inputs.json"]:
                log.warning(
                    f"WDL dir {json.parent.name} has additional json files beyond inputs/options"
                )


if __name__ == "__main__":
    print("Validating WDLs...")
    wdl_paths = fetch_wdl_paths()
    validate_wdls(wdl_paths)
