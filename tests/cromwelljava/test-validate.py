from ..common_utils import is_bad
from .utils import Womtool

wom = Womtool()


def test_womtool_validate(wdl_path):
    is_valid = wom.validate(wdl_path)
    if is_bad(wdl_path, "badVal"):
        assert not is_valid
    else:
        assert is_valid
