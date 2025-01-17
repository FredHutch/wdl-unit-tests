# Unit test for Remote File Localization (testRemoteFileLocalization)

## Overview
The `testRemoteFileLocalization` workflow is designed to validate and demonstrate input localization and output handling in WDL. It includes tasks for:

- Input file localization from a remote location.
- File manipulation based on input parameters.
- Output generation and passing between tasks.
  
This unit test ensures that:
- Input variables are properly substituted in task commands.
- Output files are correctly generated and passed through workflow tasks.
- Files are localized from a remote location and handled appropriately.

## Purpose
This workflow serves as a unit test to validate:
- File input and output handling
- Localization of remote files
- Input variables substitution
- Passing outputs between tasks
- Renaming of files and verification of the processed output

## Workflow Components

### Workflow: `testRemoteFileLocalization`
The main workflow demonstrates how to localize and manipulate files, with validation for the input parameters and output generation.

**Inputs:**
- `string`: String - A simple string input for testing variable substitution.
- `integer`: Int - An integer input for variable substitution in tasks.
- `float`: Float - A floating-point number for variable substitution.
- `boolean`: Boolean - A boolean input to test task command logic.
- `remote_file`: File - A remote file that will be localized by the WDL engine and passed to tasks.

**Outputs:**
- `localized_file`: File - The file processed and passed through the workflow.
- `localized_string`: File - A file containing the string input value.
- `localized_integer`: File - A file containing the integer input value.
- `localized_float`: File - A file containing the float input value.
- `localized_boolean`: File - A file containing the boolean input value.
- `renamed_file`: File - The file renamed in a subsequent task.

### Tasks

#### Task: `testInputLocalization`
This task generates output files based on the input parameters, validating that the variables are properly passed and substituted into the task's command. It also verifies the localization of the input file.

**Command**:
- Substitutes the input string, integer, float, and boolean into echo commands that generate output files.
- Verifies that the remote input file is localized by WDL.

**Outputs**:
- `outputStringfile`: File - Contains the string input.
- `outputIntegerfile`: File - Contains the integer input.
- `outputFloatfile`: File - Contains the float input.
- `outputBooleanfile`: File - Contains the boolean input.
- `processed_file`: File - The input file passed directly as an output.

#### Task: `testOutputUsage`
This task demonstrates how to handle outputs from the previous task. It renames the file received as input and generates a new output.

**Command**:
- Renames the file received from the `testInputLocalization` task.

**Outputs**:
- `renamed_file`: File - The renamed file.

**Runtime Requirements**:
- CPU: 1 core
- Memory: 1 GB

## Usage
```bash
# Execute with Cromwell
java -jar cromwell.jar run testRemoteFileLocalization.wdl -i inputs.json

# Execute with miniwdl
miniwdl run testRemoteFileLocalization.wdl \
  string="Test String Input" \
  integer=123 \
  float=9.81 \
  boolean=false \
  remote_file="/hpc/temp/_DaSL/remote_file.txt"
```

### Example inputs.json:
```json
{
  "testRemoteFileLocalization.string": "Test String Input",
  "testRemoteFileLocalization.integer": 123,
  "testRemoteFileLocalization.float": 9.81,
  "testRemoteFileLocalization.boolean": false,
  "testRemoteFileLocalization.remote_file": "/hpc/temp/_DaSL/remote_file.txt"
}
```

## Version
WDL 1.0

## Additional Notes
- Ensures proper localization of remote files by WDL engine.
- Validates input substitution in task commands.
- Demonstrates the process of passing file outputs between tasks.
- Includes a task for file renaming as a form of output processing.
- Provides a simple test for handling various input types (string, integer, float, boolean) in WDL workflows.
