from utils import CromwellJava

cromwell = CromwellJava()


def test_cromwell_run(wdl_path):
    is_valid = cromwell.run(wdl_path)
    if wdl_path.startswith("badVal") or wdl_path.startswith("badRun"):
        assert not is_valid
    else:
        assert is_valid
