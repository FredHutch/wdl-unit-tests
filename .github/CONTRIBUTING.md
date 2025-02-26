# Contributing to wdl-unit-tests

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Suggesting New Unit Tests

New unit test suggestions are tracked as GitHub issues. When creating a unit test suggestion, please:
- First check the [issue tracker](https://github.com/FredHutch/wdl-unit-tests/issues) to identify if your issue/proposed unit test is already in development. This avoids duplication and promotes collaborative efforts on problems of common interest.
- Use a clear and descriptive title
- Provide a detailed description of what the unit test is actually intending to test?
- Explain why this additional test would be useful

### Contributing New Unit Tests

1. Once you have identified a new unit test and would like to contribute towards building this repository, begin by filing an issue in this repository.
2. Clone the repo locally and create a branch from `main`. Please name the branch using this convention: "issue#-issue-title"
3. Create a very specific WDL unit test and make sure to add enough commentary in the code.
4. Ensure your proposed WDL runs locally via `miniwdl run` or `java -jar cromwell-87.jar run`
5. If you are user of PROOF, please also make sure to test that the WDL unit test runs via PROOF.
    - If your WDL succeeds locally but fails in PROOF, please report the issue in the [proof-api repo](https://github.com/FredHutch/proof-api/issues).
6. Add the WDL to a subdirectory by the same name, i.e. `coolUnitTest/coolUnitTest.wdl`. If the WDL is expected to fail WOMtool the subdirectory AND the WDL file name must start with `badVal`. If the WDL is expected to fail both WOMtool and a Cromwell run, then the subdirectory AND the WDL file name must start with `badRun`.
7. Make sure to include an `inputs.json` and `options.json` if required and make sure that any other. input files referenced in `inputs.json` are provided in the same directory.
8. Add a README to the WDL's subdirectory describing the unit test's functionality and purpose.
9. If you make any changes to Python files in `tests/` make sure to run `make lint-check` and `make format-check` and make any changes as suggested by those commands
10. Commit and push your proposed changes to GitHub.
11. Create a pull request describing the updates and identifying the corresponding GitHub issue.
12. Request a review from a member of the DaSL team (ideally the person requesting the test).
13. Address all comments/requested changes from these reviews.
14. Once the PR has been approved and all checks have passed, merge the PR into `main`.

## Style Guidelines

- Follow [WILDS WDL Style Guide](https://getwilds.org/guide/wdlconfig.html)
- For now, only use WDL v1.0 syntax (sadly Cromwell only accepts v1.0)

## License

By contributing, you agree that your contributions will be licensed under the same license as the original project.
