# Unit test for Nonstandard Outputs

## Overview
The test_nonstandard_outputs workflow is a unit test designed to validate and demonstrate handling of various non-standard output file scenarios in WDL (Workflow Description Language). It tests the workflow engine's ability to handle:

- Files with special characters in names
- Files without extensions
- Files in nested directories
- Symbolic links
- Pattern-based file globbing

## Purpose
This workflow serves as a comprehensive test case for:
- Special character handling in file names
- Path handling for files without extensions
- Nested directory structure handling
- Symbolic link resolution
- Glob pattern file collection
- File system operations
- Output file declaration patterns
- Docker container file system interaction

## Workflow Components

### Workflow: `test_nonstandard_outputs`
The main workflow demonstrates various non-standard output file handling capabilities.

**Outputs:**
- `special_chars`: File - Output file containing special characters in name
- `no_extension`: File - Output file without a file extension
- `nested_output`: File - Output file from a nested directory structure
- `symlink_file`: File - Symbolic link to another file
- `glob_files`: Array[File] - Collection of files matching a pattern

### Tasks

#### Task: `generate_diverse_outputs`
Creates various types of output files to test the workflow engine's handling capabilities.

**Operations:**
- Creates a file with special characters (@, #) in the name
- Generates a file without an extension
- Creates a nested directory structure with files
- Creates and manages symbolic links
- Generates multiple files matching a pattern

**Runtime Requirements:**
- Docker: ubuntu:noble-20241118.1

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run nonstandardOutputs.wdl

# Execute with miniwdl
miniwdl run nonstandardOutputs.wdl
```

No input parameters are required for this workflow.

Expected outputs:
```
outputs/
├── special_chars        # File named "test@file#1.txt"
├── no_extension        # File named "datafile"
├── nested_output      # File from nested/dir/test.txt
├── symlink_file       # Symbolic link "link.txt"
└── glob_files/        # Directory containing pattern_*.out files
    ├── pattern_1.out
    ├── pattern_2.out
    └── pattern_3.out
```

## Version
WDL 1.0

## Additional Notes
- Tests workflow engine's ability to handle non-standard file names
- Verifies proper handling of nested directory structures
- Validates symbolic link resolution
- Demonstrates glob pattern functionality
- Tests Docker container file system interactions
- Useful for validating output handling in different execution environments
- Helps identify potential file system compatibility issues
- Verifies proper path resolution and file access patterns
