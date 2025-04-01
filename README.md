# wdl-unit-tests

![Runs on Cromwell](https://github.com/FredHutch/wdl-unit-tests/actions/workflows/cromwell-test-run.yml/badge.svg)
![WOMtool Validation](https://github.com/FredHutch/wdl-unit-tests/actions/workflows/womtools-validate.yml/badge.svg)
![API Tests](https://github.com/FredHutch/wdl-unit-tests/actions/workflows/api-tests.yml/badge.svg)

A collection of WDL (Workflow Description Language) workflows designed for testing WDL execution environments and backend configurations. Each workflow tests a specific aspect of WDL functionality while maintaining simplicity for easy debugging and verification.

## Usage
Each workflow can be run using standard WDL execution engines:

```bash
# Using Cromwell
java -jar cromwell.jar run <workflow_name>.wdl

# Using miniwdl
miniwdl run <workflow_name>.wdl
```

## Purpose
This test suite is designed to:
- Validate WDL execution environments
- Test different backend configurations
- Verify software deployment methods (native, container, modules)
- Serve as examples for WDL development

## Contributing
See our [CONTRIBUTING.md](.github/CONTRIBUTING.md) for exact details on how to contribute.

## Tests

> [!TIP]
> See the [architecture doc](docs/architecture.md) to better understand the design of this test suite.

There are two sets of tests for running WDLs against Cromwell using Python:

- `tests/cromwelljava`: Runs WDLs on Cromwell using a local copy of `cromwell-<version>.jar` and `womtool-<version>.jar`. See "Java" below for details.
- `tests/cromwellapi`: Runs WDLs on Cromwell running on FH clusters via the [PROOF API][proofapi]. See "API" below for details.

What's the difference between the two sets of tests? The Java tests run against just the Java Cromwell code itself, whereas the API tests are a kind of integration test that incorporates all the infrastructure behind PROOF including the [PROOF API][proofapi], the Cromwell servers that PROOF manages, and the FH cluster infra that it all runs on.

To run both sets of tests:

- clone this repository locally and cd into it
- if you don't have `uv` installed, [install it][uvinstall]
- create a virtual environment: `uv venv`. This should pick up the Python version specified in `.python-version`. If you do not have the version given in `.python-version` it will be installed by `uv`
- activate the virtual environment: `source .venv/bin/activate`
- install dependencies: `uv sync`
- check that you have the Python version in `.python-version`: `python --version`

Familiarity with two tools will help you run and especially contribute to tests:
- [pytest][]: a Python test framework. when you run `uv sync` above you'll then have a cli binary `pytest` available
- [uv][]: a Python package and project manager; manages dependencies, runs tests, etc.

If you make any changes to Python files in `tests/` make sure to run `make lint-check` and `make format-check` and make any changes as suggested by those commands

### Java

These tests are run on GitHub Actions on each pull request via the `.github/workflows/cromwell-test-run.yml` and `.github/workflows/womtools-validate.yml` workflows.

To run them locally:

- You'll need env vars set for the paths for each of `cromwell-<version>.jar` and `womtool-<version>.jar`. For cromwell it's `CROMWELL_PATH` and for womtools it's `WOMTOOL_PATH`. You can either set the path in a dot file or export for the current shell session or prefix the pytest line below with the env key and value.

```sh
CROMWELL_PATH=/path/to/cromwell-87.jar uv run pytest tests/cromwelljava/test-run.py --wdl-path=helloHostname --verbose -s

WOMTOOL_PATH=/path/to/womtool-87.jar uv run pytest tests/cromwelljava/test-validate.py --wdl-path=helloHostname --verbose -s
```

Note that each call to `test-run.py` or `test-validate.py` runs one WDL only.

Adding tests shouldn't require any changes to the files in `tests/cromwelljava` - though if you run into any issues let's talk about it.

### API

These tests are run on GitHub Actions on each push to main/dev and each pull request via the `.github/workflows/api-tests.yml` workflow. This GH Action is run on our custom runner that runs on FH infrastructure so it has appropriate privileges.

To run tests locally:

- get on the Cisco VPN if working remotely or be on an FH campus network
- set a PROOF token for the test user used for these tests as `PROOF_API_TOKEN_DEV`. the value is in 1password ([Secrets and env vars in 1password](https://developer.1password.com/docs/cli/secrets-environment-variables/)). Talk to Sean or Scott if you don't have access.
    1. Open 1password and find the API key.
    2. Right-click the key and select "Copy Secret Reference."
    3. Add the following line to your dot file (e.g., `.zshrc`): `export PROOF_API_TOKEN_DEV="op://secret/reference/copied/from/1PW"`
- set an env var for paths to scrub in test fixtures as `PATH_ROOTS`. the value is in 1password ([Secrets and env vars in 1password](https://developer.1password.com/docs/cli/secrets-environment-variables/)).
    1. Open 1password and find the entry.
    2. Right-click the key and select "Copy Secret Reference."
    3. Add the following line to your dot file (e.g., `.zshrc`): `export PATH_ROOTS="op://secret/reference/copied/from/1PW"`
- reload your dot file in your terminal session so the new env vars are available
- run tests using cached test fixtures: `make test_api_cached`
- run tests while re-writing test fixtures: `make test_api_rewrite`

To add tests:

- Tests must be in files beginning with `test-`, and be in the `tests/cromwellapi/` dir
- Ideally use the pytest fixture `cromwell_api` created in `tests/cromwellapi/conftest.py` to call the Cromwell API. If there's a method missing that you need add it to the `CromwellApi` class in `tests/cromwellapi/cromwell.py`

Note that some of these tests run through all WDLs in this dir, while others only run through one or some subset of WDLs.

> [!IMPORTANT]
> Some notes about vcr "cassetttes" in `tests/cromwellapi/cassettes`:
>
> Changes in cassettes should only happen when new HTTP requests are made.
>
> PR reviewers can largely ignore changes in cassettes - though they should be given a cursory look to check for anything that should be discussed

### WDL Unit Test Guidelines

- Each unit test gets its own subdirectory with the same name as the WDL file.
- Inputs should be provided (when necessary) via a json file specifically named `inputs.json`.
- Caching behaviors should be provided via a json file specifically named`options.json`.
- If you expect the WDL to fail both validation and execution, the WDL name should start with `badVal` (e.g. `badValMissingValue`).
- If you expect the WDL to pass validation but fail execution, the WDL name should just start with `bad` (e.g. `badRunParseBatchFile`).

[uvinstall]: https://docs.astral.sh/uv/getting-started/installation/
[proofapi]: https://github.com/FredHutch/proof-api
[pytest]: https://docs.pytest.org/en/stable/
[uv]: https://docs.astral.sh/uv/
