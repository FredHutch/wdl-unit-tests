# Unit Test for File Operations (testFileoperations)

## Overview
The `testFileoperations` workflow is a unit test designed to validate and demonstrate essential file manipulation capabilities in WDL (Workflow Description Language). It includes tests for:

- Creating multiple files within a task environment.
- Moving a file to a specific directory.
- Renaming a file to a new name.
- Ensuring all intermediate and final file states are properly handled and outputted.

## Purpose
This workflow is intended to:
- Verify file creation and content generation during task execution.
- Test file relocation to specified directories.
- Validate file renaming to new names.
- Ensure proper handling and cleanup of intermediate file states.
- Confirm that all required files are accessible as task outputs after execution.

## Workflow Components

### Workflow: `testFileoperations`
This workflow demonstrates creating three files, moving one of them to a new directory, and renaming another.

**Inputs:**
- No inputs are required. All operations are self-contained within the task.

**Outputs:**
- `created_file1`: File - The first file created during task execution.
- `moved_file`: File - The second file after being moved to a new directory.
- `renamed_file`: File - The third file after being renamed.

### Tasks

#### Task: `file_operations`
Performs the following operations:
1. Creates three files: `file1.txt`, `file2.txt`, and `file3.txt`.
2. Moves `file2.txt` to the `output_dir` directory.
3. Renames `file3.txt` to `file3_renamed.txt`.

**Task Outputs:**
- `created_file1`: The file `file1.txt`, which remains in the root directory.
- `moved_file`: The file `file2.txt` after being moved to `output_dir`.
- `renamed_file`: The file `file3.txt` after being renamed to `file3_renamed.txt`.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: `ubuntu:20.04`

## Usage
```bash
# Execute with Cromwell
java -jar cromwell.jar run testFileoperations.wdl

# Execute with MiniWDL
miniwdl run testFileoperations.wdl
```

This workflow does not require any input JSON as it is fully self-contained.

## Outputs Directory
Upon successful execution, the output directory will contain:
- `file1.txt`: The first created file.
- `output_dir/file2.txt`: The file after being moved to the `output_dir` directory.
- `file3_renamed.txt`: The file after being renamed.
- Execution logs (`stdout` and `stderr`) for debugging purposes.

## Example Outputs
- `file1.txt`:
  ```
  This is the first created file.
  ```
- `output_dir/file2.txt`:
  ```
  This is the second file that will be moved.
  ```
- `file3_renamed.txt`:
  ```
  This is the third file that will be renamed.
  ```

## Version
WDL 1.0
