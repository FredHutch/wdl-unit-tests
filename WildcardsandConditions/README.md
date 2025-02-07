
# Unit Test for Wildcard Resolution and Conditional Logic (WildcardsandConditions)

## Overview

The `WildcardsandConditions` workflow is a unit test designed to validate the behavior of wildcard resolution and conditional logic in WDL (Workflow Description Language). It includes tests for:

- **Wildcard Resolution**: Ensures that files matching the wildcard pattern (e.g., `*.txt`) are correctly identified and handled in the workflow.
- **Conditional Logic**: Verifies that conditional logic within the command block works properly, such as the creation of files based on boolean conditions.
- **Input Parsing**: Confirms that inputs passed to the workflow are correctly parsed and used within the command block.

## Purpose

This workflow serves as a test case for:
- Wildcard handling in file operations (creating and globbing files).
- Conditional logic inside the command block (such as `if` statements).
- Parsing and using workflow inputs in commands.
- Validation of input parameters (required and default inputs).
  
## Workflow Components

### Workflow: `WildcardsandConditions`

This workflow demonstrates wildcard handling, conditional file creation, and input parsing in a WDL task.

**Inputs:**
- `prefix`: String - The prefix used to create files (e.g., `sample`) (required).
- `create_extra_file`: Boolean - A flag to control the conditional creation of an extra file (optional, defaults to `true`).

**Outputs:**
- `txt_files`: Array[File] - A list of `.txt` files created in the task, resolved using a wildcard.
- `conditional_result`: String - The content of the file that shows the parsed `prefix` input.

### Tasks

#### Task: `wildcard_and_conditions_test`
- **Purpose**: Creates `.txt` files using a wildcard pattern, conditionally creates an extra file, and parses the `prefix` input.
- **Key Operations**:
  - Create `.txt` files with a dynamic name using a loop and wildcard.
  - Conditionally create an additional file based on the `create_extra_file` input.
  - Output the parsed `prefix` in a file to verify input parsing.

**Runtime Requirements:**
- **Docker Image**: `ubuntu:20.04`
- **CPU**: 1 core
- **Memory**: 1 GB

---

## Usage

### Input JSON

To run the workflow, you need to specify the required `prefix` input in an `inputs.json` file. Here's an example:

```json
{
  "WildcardsandConditions.prefix": "testfile",
  "WildcardsandConditions.create_extra_file": true
}
```

You can run the workflow with the following command:

```bash
# Using Cromwell
java -jar cromwell.jar run WildcardsandConditions.wdl -i inputs.json

# Using MiniWDL
miniwdl run WildcardsandConditions.wdl prefix="testfile" create_extra_file=true
```

### Expected Output Files

1. **txt_files**: This output will contain a list of `.txt` files matching the wildcard pattern (`*.txt`) created during the task execution, including the ones with the prefix provided.
   
   Example:
   - `testfile_1.txt`
   - `testfile_2.txt`
   - `testfile_3.txt`
   - If `create_extra_file` is `true`, there will also be `testfile_extra.txt`.

2. **conditional_result**: This output will contain the content of the file created by the task that verifies the parsing of the `prefix` input.

   Example:
   - Content of `parsed_output.txt`: `"Parsed prefix: testfile"`

---

## Version
- **WDL Version**: 1.0

---

## Additional Notes
- This workflow demonstrates the usage of wildcards in WDL, which can be particularly useful when working with large datasets where files follow a consistent naming pattern.
- The conditional logic in this test checks whether a specific file is created based on the value of the input parameter `create_extra_file`.
- The workflow also tests how inputs are parsed and used in the command block, allowing for dynamic file creation and manipulation based on workflow parameters.
- If no value for `prefix` is provided, the workflow will fail with an error message, as the input is required. You can provide a default value in the `input` block if you want to make it optional.

