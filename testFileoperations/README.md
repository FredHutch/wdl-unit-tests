# Unit Test for File Operations (testFileOperations)

## Overview
The testFileOperations workflow is a unit test designed to validate and demonstrate file manipulation capabilities in WDL (Workflow Description Language). It includes tests for:

- File creation within the task environment.
- Moving files to a specific directory.
- Renaming files to ensure flexibility and validation of file operations.
- Handling intermediate file states and ensuring proper task outputs.

## Purpose
This workflow serves as a comprehensive test case for:
- File creation and verification within task execution.
- File renaming and relocation to specific directories.
- Intermediate file handling and cleanup.
- Ensuring outputs are localized and accessible after workflow execution.
- Basic content manipulation for file testing.
- Validating that only required files are stored as outputs.

## Workflow Components

### Workflow: `testFileOperations`
The main workflow demonstrates file creation, relocation, and renaming operations.

**Inputs:**
- No inputs are required for this workflow. All file operations are self-contained within the task.

**Outputs:**
- `created_file`: File - The initially created file in the task.
- `moved_file`: File - The file after it has been moved to the output directory.
- `renamed_file`: File - The final renamed file.

### Tasks

#### Task: `file_operations`
Performs the following operations:
1. Creates a file named `created_file.txt` with predefined content.
2. Moves the file to an `output_dir` directory.
3. Renames the file to `renamed_file.txt` within the directory.

**Task Outputs:**
- `created_file`: The initially created file.
- `moved_file`: The file after being moved to `output_dir`.
- `renamed_file`: The final file after renaming.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: `ubuntu:20.04`

## Usage
```bash
# Execute with Cromwell
java -jar cromwell.jar run testFileOperations.wdl

# Execute with MiniWDL
miniwdl run testFileOperations.wdl
```

No inputs are required since the workflow is self-contained.

## Outputs Directory
The output directory will include:
- `renamed_file.txt`: The final file after renaming.
- `stdout` and `stderr`: Task execution logs for debugging purposes.

## Example Outputs
- `created_file.txt`: Initial file with content:
  ```
  This is the created file.
  ```
- `output_dir/renamed_file.txt`: Final file after relocation and renaming.

## Version
WDL 1.0
