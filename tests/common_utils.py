import json
import sys
from pathlib import Path
from typing import Optional


def is_interactive() -> bool:
    return hasattr(sys, "ps1")


def get_root() -> Path:
    if is_interactive():
        return Path.cwd().parents[1].resolve()
    else:
        return Path(__file__).parents[1].resolve()


def is_bad(path: Path, key: str) -> bool:
    root = get_root()
    wdl_path = root / f"{path}/{path}.wdl"
    conds = conditions(wdl_path)
    return conds.get(key, False)


def conditions(wdl_path: Path) -> dict:
    conditions_path = wdl_path.parent / "conditions.json"
    if conditions_path.exists():
        with open(conditions_path, "r") as f:
            conditions = json.load(f)
    else:
        conditions = {"badVal": False, "badRunJava": False, "badRunAPI": False}
    return conditions


def check_one(x: str):
    allowed = ["badRun", "badRunAPI", "badRunJava", "badVal"]
    if x not in allowed:
        raise ValueError(f"include/exclude need to be in the set: {allowed}")


def check_exclude_include(x: list):
    [check_one(item) for item in x]


def fetch_wdl_paths(
    exclude: Optional[list] = None, include: Optional[list] = None
) -> list:
    """
    Fetch WDL paths, with optional include or exclude

    Examples:
      fetch_wdl_paths()
      fetch_wdl_paths(exclude=["badRunAPI"])
      fetch_wdl_paths(exclude=["badRunAPI", "badRunJava"])
      fetch_wdl_paths(include=["badVal", "badRunAPI"])
    """
    root = get_root()

    paths = list(root.glob("**/*.wdl"))

    if not exclude and not include:
        return paths

    paths_keep = []

    if exclude:
        check_exclude_include(exclude)
        for path in paths:
            bools = [conditions(path).get(item, False) for item in exclude]
            if not any(bools):
                paths_keep.append(path)

    if include:
        check_exclude_include(include)
        for path in paths:
            bools = [conditions(path).get(item, True) for item in include]
            if any(bools):
                paths_keep.append(path)

    return paths_keep
