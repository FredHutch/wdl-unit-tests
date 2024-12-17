# Required Inputs Validation WDL Workflow

## Overview
This workflow tests and validates two required inputs: a string and an integer. It ensures that the string contains only alphabetic characters and spaces, while the integer contains only digits. The workflow outputs an error message for invalid inputs or confirms successful validation for valid inputs.

## Workflow Components

### Workflow: `required_inputs_test`
The main workflow calls the `validate_inputs` task to perform input validation.

**Inputs:**
- `required_string`: String - A required non-empty string containing only alphabetic characters and spaces.
- `required_int`: Int - A required integer that must contain only digits.

**Outputs:**
- `output_message`: String - A message summarizing the validation outcome.

### Task: `validate_inputs`
Performs input validation for the provided string and integer.

**Runtime Requirements:**
- Docker: `ubuntu:20.04`

**Inputs:**
- `required_string`: String - Input string to validate.
- `required_int`: Int - Input integer to validate.

**Outputs:**
- `outputFile`: File - A file (`output.txt`) containing validation results or error messages (the test does not give an error but maybe used for testing if needed).

**Command Logic:**
1. Validates that `required_string`:
   - Is non-empty.
   - Contains only alphabetic characters and spaces.

2. Validates that `required_int`:
   - Contains only digits.

3. Outputs a success message if both checks pass.

### Example Output
If the inputs are valid, the output file `output.txt` will contain:
```
Received required_string: Hello
Received required_int: 123456
Validation successful!
```

If an input is invalid, an error message will be written to `output.txt`, and the task will exit with an error.

## Purpose
This workflow serves as a test case for:
- Required input validation in WDL.
- String and integer input type enforcement.
- Error handling and messaging for invalid inputs.
- File output generation based on validation results.

## Version
WDL 1.0

## Notes
- The Docker image used is `ubuntu:20.04`.
- This workflow is suitable for testing input validation and task failure scenarios.
- Useful for backend testing where strict input requirements are enforced.
