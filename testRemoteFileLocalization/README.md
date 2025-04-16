# Unit Test for Remote File Localization (`testRemoteFileLocalization`)

## Overview
The `testRemoteFileLocalization` workflow is designed to validate and demonstrate input localization, output handling, and the remote storage of workflow outputs using WDL. It includes tasks for:

- Input file localization from a remote location.
- File manipulation based on input parameters.
- Output generation and passing between tasks.
- Storing final workflow outputs in a specified remote directory.

## Purpose
This workflow serves as a unit test to validate:
- File input and output handling.
- Localization of remote files.
- Input variable substitution.
- Passing outputs between tasks.
- Renaming of files and verification of processed output.
- Remote storage of final workflow outputs.

## Workflow Components

### Workflow: `testRemoteFileLocalization`
The main workflow demonstrates how to localize and manipulate files, with validation for the input parameters, output generation, and remote storage.

**Inputs:**
- `string`: String - A simple string input for testing variable substitution.
- `integer`: Int - An integer input for variable substitution in tasks.
- `float`: Float - A floating-point number for variable substitution.
- `boolean`: Boolean - A boolean input to test task command logic.
- `remote_file`: File - A remote file localized by the WDL engine and passed to tasks.

**Outputs:**
- `localized_file`: File - The file processed and passed through the workflow.
- `localized_string`: File - A file containing the string input value.
- `localized_integer`: File - A file containing the integer input value.
- `localized_float`: File - A file containing the float input value.
- `localized_boolean`: File - A file containing the boolean input value.
- `renamed_file`: File - The file renamed in a subsequent task.

**Remote Storage Configuration:**
The `options.json` file specifies the location for storing all final workflow outputs:
```json
{
    "final_workflow_outputs_dir": "/fh/fast/_DaSL/proof_testing",
    "use_relative_output_paths": true
}
```

### Tasks

#### Task: `testInputLocalization`
This task generates output files based on the input parameters and verifies that the remote input file is localized.

**Command**:
- Substitutes input variables (string, integer, float, boolean) into echo commands that generate output files.
- Verifies the localization of the remote input file.

**Outputs**:
- `outputStringfile`: File - Contains the string input.
- `outputIntegerfile`: File - Contains the integer input.
- `outputFloatfile`: File - Contains the float input.
- `outputBooleanfile`: File - Contains the boolean input.
- `processed_file`: File - The input file passed directly as output.

#### Task: `testOutputUsage`
This task renames the file received from the previous task.

**Command**:
- Renames the file from `testInputLocalization` to a new output.

**Outputs**:
- `renamed_file`: File - The renamed file.

**Runtime Requirements**:
- Docker: `ubuntu:20.04`
- CPU: 1 core
- Memory: 1 GB

## Usage
1. **Prepare Inputs**:
Create an `inputs.json` file:
```json
{
  "testRemoteFileLocalization.string": "Test String Input",
  "testRemoteFileLocalization.integer": 123,
  "testRemoteFileLocalization.float": 9.81,
  "testRemoteFileLocalization.boolean": false,
  "testRemoteFileLocalization.remote_file": "/fh/fast/_DaSL/proof_testing/remote_file.txt"
}
```

2. **Configure Output Storage**:
Create an `options.json` file:
```json
{
    "final_workflow_outputs_dir": "/fh/fast/_DaSL/proof_testing/remoteOutputstorage",
    "use_relative_output_paths": true
}
```

3. **Run the Workflow**:
Execute the workflow using Cromwell:
```bash
java -jar cromwell.jar run testRemoteFileLocalization.wdl -i inputs.json -o options.json
```

Alternatively, run with miniwdl:
```bash
miniwdl run testRemoteFileLocalization.wdl \
  -i inputs.json \
  -o options.json
```

## Version
- **WDL**: 1.0
- **Options JSON**: Version 1.0

## Additional Notes
- This workflow validates the localization of remote files by the WDL engine.
- Demonstrates remote storage of outputs using `options.json`.
- Provides simple tests for handling various input types (string, integer, float, boolean) in WDL workflows.
- Ensures outputs are properly organized and stored in the specified directory.

