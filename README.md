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

There are two sets of tests for running WDLs against Cromwell using Python:

- `tests/cromwelljava`: Runs WDLs on Cromwell using a local copy of `cromwell-<version>.jar` and `womtool-<version>.jar`. See "Java" below for details.
- `tests/cromwellapi`: Runs WDLs on Cromwell running on FH clusters via the [PROOF API][proofapi]. See "API" below for details.

What's the difference between the two sets of tests? The Java tests run against just the Java Cromwell code itself, whereas the API tests are a kind of integration test that incorporates all the infrastructure behind PROOF including the [PROOF API][proofapi], the Cromwell servers that PROOF manages, and the FH cluster infra that it all runs on.

To run both sets of tests:

- clone this repository locally and cd into it
- if you don't have `uv` installed, [install it][uvinstall]
- create a virtual environment: `uv venv`. This should pick up the Python version specified in `.python-version`. If you do not have the version given in `.python-version` it will be installed by `uv`
- activate the virtual environment: `source .venv/bin/activate`
- check that you have the Python version in `.python-version`: `python --version`

Info:
- [pytest][]
- [uv][]

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

These tests are run on GitHub Actions on each push to main/dev and each pull request via the `.github/workflows/api-tests.yml` workflow.

To run them locally:

- get on the Cisco VPN if working remotely or be on an FH campus network
- set a PROOF token for the test user used for these tests as `PROOF_API_TOKEN_DEV`. the value is in 1password ([Secrets and env vars in 1password](https://developer.1password.com/docs/cli/secrets-environment-variables/)). Talk to Sean or Scott if you don't have access.
    1. Open 1password and find the API key.
    2. Right-click the key and select "Copy Secret Reference."
    3. Run: `export PROOF_API_TOKEN_DEV="op://secret/reference/copied/from/1PW"`
- run tests, for example: `op run -- uv run pytest tests/cromwellapi --verbose` 

To add tests:

- Tests must be in files beginning with `test-`, and be in the `tests/cromwellapi/` dir
- Ideally use the pytest fixture `cromwell_api` created in `tests/cromwellapi/conftest.py` to call the Cromwell API. If there's a method missing that you need add it to the `CromwellApi` class in `tests/cromwellapi/cromwell.py`

Note that some of these tests run through all WDLs in this dir, while others only run through one or some subset of WDLs.

[uvinstall]: https://docs.astral.sh/uv/getting-started/installation/
[proofapi]: https://github.com/FredHutch/proof-api
[pytest]: CROMWELL_PATH=/Users/schambe3/github/cromwell/cromwell-86.jar
[uv]: https://docs.astral.sh/uv/
