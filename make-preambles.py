from pathlib import Path

from tests.common_utils import is_interactive


def get_root() -> Path:
    if is_interactive():
        return Path.cwd().resolve()
    else:
        return Path(__file__).parent.resolve()


def fetch_file(path: Path) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def make_preambles() -> None:
    root = get_root()
    paths = list(root.glob("**/*.wdl"))
    for path in paths:
        path_readme = list(path.parent.glob("README.md"))
        readme = fetch_file(path_readme[0])
        readme_prefixed = [f"## {w}" for w in readme]

        wdl = fetch_file(path)

        readme_wdl = readme_prefixed + ["\n", "\n"] + wdl

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(readme_wdl)


if __name__ == "__main__":
    make_preambles()
