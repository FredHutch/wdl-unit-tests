# testRemoteFileLocalization

## Overview
Unit test workflow that validates remote file localization, input parameter handling, and output file generation in WDL.

## Purpose
This workflow tests:
- Remote file localization by the WDL engine
- Input parameter substitution (string, integer, float, boolean)
- File passing between tasks
- Basic file operations and output generation

## Workflow Structure

### Inputs
- `string` (String): Test string for variable substitution
- `integer` (Int): Test integer for variable substitution  
- `float` (Float): Test float for variable substitution
- `boolean` (Boolean): Test boolean for variable substitution
- `remote_file` (File): Remote file to be localized

### Outputs
- `localized_file` (File): Original input file passed through workflow
- `localized_string` (File): File containing the string input value
- `localized_integer` (File): File containing the integer input value
- `localized_float` (File): File containing the float input value
- `localized_boolean` (File): File containing the boolean input value
- `renamed_file` (File): File renamed by the second task

## Tasks

### testInputLocalization
Generates output files from input parameters and verifies remote file localization.

**Inputs**: All workflow inputs  
**Outputs**: Files containing each input parameter value, plus the original file

### testOutputUsage  
Demonstrates file passing between tasks by renaming the file from the first task.

**Inputs**: `processed_file` from testInputLocalization  
**Outputs**: `renamed_file` - the renamed file

## Usage

Create an inputs file:
```json
{
  "testRemoteFileLocalization.string": "Test String Input",
  "testRemoteFileLocalization.integer": 123,
  "testRemoteFileLocalization.float": 9.81,
  "testRemoteFileLocalization.boolean": false,
  "testRemoteFileLocalization.remote_file": "/path/to/remote/file.txt"
}
```

Run the workflow:
```bash
# Cromwell
java -jar cromwell.jar run testRemoteFileLocalization.wdl --inputs inputs.json

# miniWDL  
miniwdl run testRemoteFileLocalization.wdl -i inputs.json
```

**Requirements**: WDL 1.0, Docker runtime (ubuntu:20.04)
