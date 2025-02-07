# Overview

This WDL script demonstrates how to use the `glob` function to capture files from multiple directories, including nested subdirectories. It shows how to properly combine the results from multiple `glob` operations using the `flatten()` function.

## Workflow Description

The workflow `globSubdir` performs the following steps:

1. **Call to `create_nested_files` Task**:
   - The task creates two files (`file1.txt` and `file2.txt`) in two different directories: a top-level directory (`subdir/`) and a nested directory (`subdir/nested/`).
   - The task then uses two separate `glob` commands:
     - `glob("subdir/*.txt")`: This captures `.txt` files at the top level of the `subdir/` directory.
     - `glob("subdir/**/*.txt")`: This captures `.txt` files in any subdirectory, including `subdir/nested/`.

2. **Flattening Results**:
   - The workflow collects the results from both `glob` commands and uses the `flatten()` function to merge them into a single array, `matched_files`.
   - The output `matched_files` contains all the `.txt` files found in both the top-level directory and any subdirectories.

## Task Description: `create_nested_files`

### Command:
- The task creates two files:
  - `subdir/nested/file1.txt` with the content `"Hello"`
  - `subdir/file2.txt` with the content `"World"`

### Outputs:
- `matched_files_top`: An array of `.txt` files found at the top level (`subdir/*.txt`).
- `matched_files_nested`: An array of `.txt` files found in nested directories (`subdir/**/*.txt`).

## Example Output

- The output of the workflow is an array of `File` objects (`matched_files`) containing paths to all `.txt` files found in both `subdir/` and `subdir/nested/` directories.

## Purpose

This WDL (Workflow Description Language) script demonstrates how to use the `glob` function to capture files from multiple directories, including nested subdirectories. The workflow combines results from multiple `glob` operations using the `flatten()` function, ensuring that files found at different levels of directory hierarchy are collected into a single output array.

## Version

WDL 1.0

## Notes
- **File Matching**: The `glob` function is used to match files with specific patterns. In this workflow, it looks for all `.txt` files at two levels of the directory structure: one at the top level (`subdir/*.txt`) and one in nested subdirectories (`subdir/**/*.txt`).
- **Flattening**: The `flatten()` function is used to merge the results of both `glob` operations into a single output array, ensuring all matched files are included.
- **Directory Structure**:
  - `subdir/`: The top-level directory where `file2.txt` is created.
  - `subdir/nested/`: A nested directory where `file1.txt` is created.
