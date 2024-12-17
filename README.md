# wdl-unit-tests
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

## Workflow for contributing unit tests 

- Raise a GitHub Issue for the Unit test: describe the intention of what the unit test should do
- Create a unit-test branch (each unit test should have its own branch)
- Add WDL test files and or JSONS
- Commit and push
- Open a PR with atleast 2 reviewers (1 being @Sean and the other reviewer should be the person who opened this issue if you did not).
- Also if you’re contributing to that branch please make sure to mention the name of the corresponding issue in the PR
- Also make sure to add the WDL to the cromwell-test-run.yml and womtools-validate.yml
- Review reviews
- Merge 

