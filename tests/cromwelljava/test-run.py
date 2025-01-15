from utils import CromwellJava

cromwell = CromwellJava()


def test_cromwell_run(wdl_path):
    is_valid = cromwell.run(wdl_path)
    if wdl_path.startswith("bad"):
        assert not is_valid
    else:
        assert is_valid
