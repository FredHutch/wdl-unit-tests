# Unit Test for JSON File Localization (jsonFileLocalization)

## Overview
The `jsonFileLocalization` workflow is a unit test designed to validate and demonstrate the proper localization and copying of JSON files in WDL (Workflow Description Language). It includes tests for:

- Required local (local is defined as in the same storage directory as the working directory) and remote JSON file processing (a directory different from the working directory).
- Optional JSON file handling, including cases where some optional files are not provided.
- Proper file localization and copying within the workflow.
- Ensuring that missing optional files do not cause failures.

## Purpose
This workflow serves as a comprehensive test case for:
- File input/output handling
- Proper localization of required files
- Handling of optional files (including missing ones)
- Ensuring robust execution under varying input conditions
- Output array collection and validation

## Workflow Components

### Workflow: `jsonFileLocalization`
The main workflow validates file localization and copying functionality.

**Inputs:**
- `required_json_local`: `File` - Required local JSON file.
- `required_json_remote`: `File` - Required remote JSON file.
- `optional_json_local`: `File?` - Optional local JSON file.
- `optional_json_remote`: `File?` - Optional remote JSON file.
- `optional_remote_not_provided`: `File?` - Optional file not provided in the input JSON (to test missing optional handling).

**Outputs:**
- `copied_files`: `Array[File]` - Array of successfully copied JSON files.

### Tasks

#### Task: `CopyJsons`
Copies required and optional JSON files into a working directory while ensuring missing optional files do not cause failures.

**Command Execution:**
- Creates a directory `copied_jsons/`.
- Copies required local and remote JSON files.
- Copies optional files only if they exist.
- Uses conditional logic to prevent failures from missing optional files.

**Runtime Requirements:**
- Docker: `ubuntu:20.04`


### Example `inputs.json`
```json
{
  "jsonFileLocalization.required_json_local": "/hpc/temp/_DaSL/jsonFilelocalization/local_remote_required_file_1.txt",
  "jsonFileLocalization.required_json_remote": "/fh/fast/_DaSL/proof_testing/jsonFilelocalization/local_remote_required_file_2.txt",
  "jsonFileLocalization.optional_json_local": "/hpc/temp/_DaSL/jsonFilelocalization/local_remote_optional_file_1.txt",
  "jsonFileLocalization.optional_json_remote": "/fh/fast/_DaSL/proof_testing/jsonFilelocalization/local_remote_optional_file_2.txt"
}
```

## Version
WDL 1.0

## Additional Notes
- Ensures proper handling of missing optional files.
- Uses conditional logic for safe optional file processing.
- Validates both local and remote file handling.
- Provides a robust test case for file input/output operations.

