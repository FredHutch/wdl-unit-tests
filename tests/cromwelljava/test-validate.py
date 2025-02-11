from utils import Womtool

wom = Womtool()


def test_womtool_validate(wdl_path):
    is_valid = wom.validate(wdl_path)
    if wdl_path.startswith("badVal"):
        assert not is_valid
    else:
        assert is_valid
