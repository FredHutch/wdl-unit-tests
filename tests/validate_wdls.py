import logging

from common_utils import fetch_wdl_paths
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler(show_time=False, markup=True)],
)
log = logging.getLogger("rich")


def validate_wdls(wdl_paths):
    [check_wdl_name_matches(w) for w in wdl_paths]
    [check_for_other_json_files(w) for w in wdl_paths]
    [check_data_dirs(w) for w in wdl_paths]


def check_wdl_name_matches(path):
    if not path.name.replace(".wdl", "") == path.parent.name:
        log.warning(
            f"WDL dir name [u]{path.parent.name}[/] and file name"
            f" [b yellow]{path.name}[/] do not match"
        )


def check_for_other_json_files(path):
    jsons = list(path.parent.glob("*.json"))
    if jsons:
        for json in jsons:
            if json.name not in ["options.json", "inputs.json"]:
                log.warning(
                    f"WDL dir [u]{json.parent.name}[/] has additional json"
                    f" files beyond inputs/options: [b yellow]{json.name}[/]"
                )


def check_data_dirs(path):
    dirs = [x for x in path.parent.iterdir() if x.is_dir()]
    if dirs:
        for ele in dirs:
            if ele.name not in ["data"]:
                log.warning(
                    f"WDL dir [u]{path.parent.name}[/] has subdir "
                    f"[b yellow]{ele.name}[/]; only dir allowed is "
                    f"[b green]data[/]"
                )


if __name__ == "__main__":
    print("Validating WDLs...")
    wdl_paths = fetch_wdl_paths()
    validate_wdls(wdl_paths)
