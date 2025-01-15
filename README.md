# wdl-unit-tests

![Runs on Cromwell](https://github.com/FredHutch/wdl-unit-tests/actions/workflows/cromwell-test-run.yml/badge.svg)
![WOMtool Validation](https://github.com/FredHutch/wdl-unit-tests/actions/workflows/womtools-validate.yml/badge.svg)

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


