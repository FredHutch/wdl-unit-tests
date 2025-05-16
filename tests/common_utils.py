import json
import sys
from pathlib import Path


def is_interactive():
    return hasattr(sys, "ps1")


def get_root():
    if is_interactive():
        return Path.cwd().parents[1].resolve()
    else:
        return Path(__file__).parents[1].resolve()


def is_bad(path: Path, key: str):
    root = get_root()
    wdl_path = root / f"{path}/{path}.wdl"
    conds = conditions(wdl_path)
    return conds.get(key, False)


def conditions(wdl_path: Path):
    conditions_path = wdl_path.parent / "conditions.json"
    if conditions_path.exists():
        with open(conditions_path, "r") as f:
            conditions = json.load(f)
    else:
        conditions = {"badVal": False, "badRunJava": False, "badRunAPI": False}
        # raise FileNotFoundError(
        #     f"Conditions file not found at {conditions_path}"
        # )
    return conditions
