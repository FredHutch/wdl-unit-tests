# wdl-unit-tests

![Runs on Cromwell](https://github.com/FredHutch/wdl-unit-tests/actions/workflows/cromwell-test-run.yml/badge.svg)
![WOMtool Validation](https://github.com/FredHutch/wdl-unit-tests/actions/workflows/womtools-validate.yml/badge.svg)

A collection of minimal WDL (Workflow Description Language) workflows designed for testing WDL execution environments and backend configurations. Each workflow tests a specific aspect of WDL functionality while maintaining simplicity for easy debugging and verification.

## Workflows

### 1. HelloHostname
Basic WDL workflow that returns the hostname of the execution node. Used for testing basic WDL functionality and execution environment.
- Tests basic command execution
- Tests basic output handling
- No container or module requirements

### 2. HelloDockerHostname
Extension of the basic hostname workflow that runs within a Docker container. Used for testing Docker integration in WDL environments.
- Tests Docker container support
- Tests container runtime environment
- Uses ubuntu:latest container image

### 3. HelloModuleHostname
Version of the hostname workflow that uses environment modules. Used for testing module-based software management systems.
- Tests environment module support
- Tests module loading functionality
- Uses Python/3.7.4-foss-2019b-fh1 module

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
- Provide simple debugging tools
- Serve as examples for WDL development

## Contributing
When adding new test workflows, please follow these guidelines:
- Keep workflows minimal and focused on testing specific features
- Include comprehensive parameter metadata
- Document runtime requirements clearly
- Isolate it to its own directory

## Cromwell tests

A suite of tests for running WDLs against Cromwell are located in `tests/cromwell-api`. Tests are run using Python. To run tests:

- clone this repository locally and cd into it
- if you don't have `uv` installed, [install it][uvinstall]
- create a virtual environment: `uv venv`. This should pick up the Python version specified in `.python-version`. If you do not have the version given in `.python-version` it will be installed by `uv`. 
- activate the virtual environment: `source .venv/bin/activate`
- check that you have the Python version in `.python-version`: `python --version`
- set a PROOF token for the test user used for these tests as `PROOF_API_TOKEN_DEV`. the value is in 1password - talk to Sean or Scott if you don't have access
- run tests, for example: `uv run pytest tests/cromwell-api/ --verbose` 

To add tests:

- Tests must be in files beginning with `test-`, and be in the `tests/` dir. All tests against the Cromwell API should go into `tests/cromwell-api/` dir
- Ideally use the pytest fixture `cromwell_api` created in `tests/cromwell-api/conftest.py` to call the Cromwell API. If there's a method missing that you need add it to the `CromwellApi` class in `tests/cromwell-api/cromwell.py`
- Make sure the tests pass. 
- Put changes to code on a branch, then open a PR

[uvinstall]: https://docs.astral.sh/uv/getting-started/installation/
