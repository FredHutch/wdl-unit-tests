# Contributing to wdl-unit-tests

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Suggesting New Unit Tests

New unit test suggestions are tracked as GitHub issues. When creating a unit test suggestion, please:
- Check the issue tracker to avoid duplicates
- Use a clear and descriptive title
- Provide a detailed description of the proposed unit test
- Explain why this additional test would be useful

### Contributing New Unit Tests

1. Clone the repo locally and create your branch from `main`
2. Ensure your proposed WDL runs locally via `miniwdl run` or `cromwell run`
3. Add the WDL to a subdirectory by the same name, i.e. `coolUnitTest/coolUnitTest.wdl`
4. Make sure to include an `inputs.json` and `options.json` if required and that any other input files referenced in `inputs.json` are provided in the same directory
6. Add a README to the WDL's subdirectory describing the unit test's functionality and purpose
7. Update the overarching repo's README as well
8. Commit and push your proposed changes to GitHub.
9. Create a pull request describing the updates and identifying the corresponding GitHub issue
10. Request a review from a member of the DaSL team (ideally the person requested the test)
11. Address all comment/requested changes from these reviews
12. Once the PR has been approved and all checks have passed, merge the PR into `main`

## Style Guidelines

- Follow [WILDS WDL Style Guide](https://getwilds.org/guide/wdlconfig.html)
- For now, only use WDL v1.0 syntax (sadly Cromwell only accepts v1.0)

## License

By contributing, you agree that your contributions will be licensed under the same license as the original project.
