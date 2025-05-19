import logging

from cromwellapi.utils import fetch_wdl_paths
from rich import print as rich_print
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler(show_time=False, markup=True)],
)
log = logging.getLogger("rich")


class LogCapture:
    def __init__(self):
        self.records = []
        self.handler = None

    def setup(self):
        self.handler = logging.Handler()
        self.handler.setLevel(logging.WARNING)
        self.handler.emit = lambda record: self.records.append(record)
        log.addHandler(self.handler)

    def teardown(self):
        if self.handler:
            log.removeHandler(self.handler)

    def has_logs(self):
        return len(self.records) > 0


def validate_wdls(wdl_paths, raise_on_logs=True):
    """Validate WDL files and optionally raise exception if any issues are found.

    Args:
        wdl_paths: List of paths to WDL files to validate
        raise_on_logs: If True, raise exception if any validation logs are produced

    Raises:
        ValueError: If raise_on_logs is True and any validation logs are produced
    """
    log_capture = LogCapture()
    try:
        log_capture.setup()
        [check_wdl_name_matches(w) for w in wdl_paths]
        [check_for_other_json_files(w) for w in wdl_paths]
        [check_data_dirs(w) for w in wdl_paths]

        if raise_on_logs and log_capture.has_logs():
            raise ValueError(
                f"validation failed with {len(log_capture.records)} issues. "
                "See logs above for details."
            )
    finally:
        log_capture.teardown()


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
    rich_print("Validating WDLs...")
    wdl_paths = fetch_wdl_paths()
    try:
        validate_wdls(wdl_paths)
        rich_print("Validation completed successfully!")
    except ValueError as e:
        rich_print(f"Error: {e}")
        exit(1)
