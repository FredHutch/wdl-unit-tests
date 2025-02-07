## Overview

This WDL script demonstrates how the `glob` function can be used to match files based on a pattern. In this example, the workflow is designed to create a file and attempt to find `.log` files, even though no `.log` files are created in the task. The workflow showcases handling the scenario where no files match the glob pattern.

## Workflow Components

### Workflow: `glob_nonmatching_test`
- The workflow consists of a single task, `create_files`, which is responsible for generating a file (`test.txt`) and attempting to match files with the `.log` extension using the `glob` function.

### Task: `create_files`
- **Purpose**: This task creates a text file (`test.txt`) and uses the `glob` function to search for `.log` files in the current directory.
- **Command**: 
    - Creates the file `test.txt` with the content `"Test file"`.
    - Attempts to match files with the `.log` extension using the `glob` function.
  
### Inputs:
- The task does not require any inputs.

### Outputs:
- **`unmatched_files`**: An array of files that match the glob pattern `"*.log"`. Since no `.log` files are created in the task, this output will be empty.

## Inputs
This workflow does not require any inputs. It simply creates a file in the task and attempts to match files based on a glob pattern.

## Outputs
- **`unmatched_files`**: An array of `File` objects. In this specific example, the output will be an empty array because no `.log` files are created in the task.

## Expected Output
Since the task creates a `test.txt` file and the `glob` function searches for files with a `.log` extension, and no such files are created, the expected output for `unmatched_files` will be an empty array:

## Purpose
The primary purpose of this workflow is to demonstrate how the `glob` function operates and how it behaves when no files match the specified pattern. It also serves to illustrate the task and workflow structure in a simple WDL script.

## Version
WDL Version: 1.0

## Notes
- **File Matching**: The `glob` function is used to search for files matching the pattern `"*.log"`. However, since no `.log` files are created in the task, this will result in an empty array in the output.
- **Empty Output**: The example illustrates a case where no files are matched by the `glob` pattern, leading to an empty output array. In practice, this workflow could be extended to handle other file types or scenarios where files do exist.
  
