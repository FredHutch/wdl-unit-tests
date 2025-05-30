from ..common_utils import is_bad
from .utils import CromwellJava

cromwell = CromwellJava()


def test_cromwell_run(wdl_path):
    is_valid = cromwell.run(wdl_path)
    if is_bad(wdl_path, "badVal") or is_bad(wdl_path, "badRunJava"):
        assert not is_valid
    else:
        assert is_valid
