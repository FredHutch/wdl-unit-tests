import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--wdl-path",
        action="store",
        default="default_value",
        help="Path to a directory with a WDL file to test"
    )

@pytest.fixture
def wdl_path(pytestconfig):
    return pytestconfig.getoption("--wdl-path")
