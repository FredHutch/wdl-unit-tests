# Unit Test for JSON Input Handling & Task Order (jsonTaskOrderTest)

## Overview

The `jsonTaskOrderTest` workflow is a unit test designed to validate the behavior of JSON input handling in WDL (Workflow Description Language). It ensures that a JSON input string is correctly passed and utilized by multiple tasks while maintaining the correct execution order due to the second task's dependency on the output of the first task.

## Purpose

This workflow serves as a test case for:
- Ensuring that the same JSON input is correctly used by multiple tasks.
- Verifying that task execution order is strictly maintained.
- Ensuring that Task 2 does not execute before Task 1 completes.
- Validating proper dependency resolution between tasks.

## Workflow Components

### Workflow: `JsonOrderTest`

This workflow consists of two tasks designed to test JSON input sharing and execution order.

#### Inputs:
- `input_json`: A JSON string used as input by both tasks.

#### Outputs:
- `task1_output`: Metadata file output from the `Task1` task.
- `task2_output`: Metadata file output from the `Task2` task.

### Tasks

#### Task: `Task1`
- **Purpose**: Reads and processes the JSON input.
- **Operation**:
  - Writes the JSON input to an output file.
  - Confirms Task 1 execution by appending a success message.

#### Task: `Task2`
- **Purpose**: Uses the same JSON input but depends on `Task1`.
- **Operation**:
  - Waits for `Task1` to complete.
  - Reads the same JSON input and appends `Task1`'s output to its own result file.

### Expected Output Files

- **Task1 Output (`task1_output.txt`)**
  ```
  Processing JSON in Task1: {"I am the text that from input.json"}
  Task1 completed
  ```

- **Task2 Output (`task2_output.txt`)**
  ```
  Processing JSON in Task2: {"I am the text that from input.json"}
  Task2 completed after Task1
  Processing JSON in Task1: {"I am the text that from input.json"}
  Task1 completed
  ```

## Version
- **WDL Version**: 1.0

## Additional Notes
- This workflow demonstrates how multiple tasks can share the same JSON input while maintaining execution order.
- The `Task2` execution is dependent on `Task1` completing successfully.
- The unit test confirms that JSON input is processed consistently across tasks.
- Any deviation in execution order or missing outputs indicates a failure in dependency resolution.

