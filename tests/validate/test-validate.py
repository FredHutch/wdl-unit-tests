from utils import Womtool

should_fail = ["badFile"]

wom = Womtool()


def test_womtool_validate(wdl_path):
    out = wom.validate(wdl_path)
    if wdl_path in should_fail:
        assert not out
    else:
        assert out
