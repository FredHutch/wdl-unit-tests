# Unit Test for Runtime Variable Resolution (jsonRuntimevariable)

## Overview

The `jsonRuntimevariable` workflow is a unit test designed to validate the behavior of runtime variable resolution in WDL (Workflow Description Language). It ensures that runtime attributes specified in an `options.json` file are correctly passed and utilized by different tasks in the workflow.

## Purpose

This workflow serves as a test case for:
- Ensuring that runtime attributes specified in `options.json` are correctly applied.
- Verifying that tasks adhere to the defined runtime constraints (CPU, memory, retries, failOnStderr, etc.).
- Testing the proper execution of tasks with different runtime attributes.
- Handling failures and retries correctly.

## Workflow Components

### Workflow: `jsonRuntimevariable`

This workflow consists of multiple tasks designed to test different runtime attributes and their application.

#### Inputs:
- Defined in `options.json`, including:
  - `cpu`: Number of CPU cores assigned to tasks.
  - `memory`: Memory allocated to tasks.
  - `maxRetries`: Maximum number of retries allowed for failed tasks.
  - `failOnStderr`: Whether a task should fail if it writes to stderr.
  - `continueOnReturnCode`: List of return codes that should not be treated as errors. However in this version of the unit test we are unable to test this. Subsequent updates to the test will include this

#### Outputs:
- `cpuTestOutput`: Metadata file output from the `CpuTest` task.
- `memoryTestOutput`: Metadata file output from the `MemoryTest` task.
- `retryTestOutput`: Metadata file output from the `RetryTest` task.
- `stderrTestOutput`: Metadata file output from the `StderrTest` task.

### Tasks

#### Task: `CpuTest`
- **Purpose**: Validates that the CPU runtime attribute is correctly passed and used.
- **Operation**:
  - Prints the assigned CPU value to a metadata file.
  - Runs with the CPU value specified in `options.json`.

#### Task: `MemoryTest`
- **Purpose**: Validates that the memory runtime attribute is correctly passed and used.
- **Operation**:
  - Prints the assigned memory value to a metadata file.
  - Runs with the memory value specified in `options.json`.

#### Task: `RetryTest`
- **Purpose**: Ensures that failed tasks retry up to the maximum number of allowed retries.
- **Operation**:
  - Simulates a transient failure that succeeds randomly.
  - Verifies that the task does not fail permanently unless all retries are exhausted.

#### Task: `StderrTest`
- **Purpose**: Tests the `failOnStderr` runtime attribute.
- **Operation**:
  - Simulates an error message being written to stderr.
  - Ensures the task behavior matches the `failOnStderr` setting in `options.json`.

## Usage

### Options JSON

The following `options.json` file configures default runtime attributes for the workflow:

```json
{
  "default_runtime_attributes": {
    "cpu": 4,
    "memory": "4G",
    "maxRetries": 4,
    "continueOnReturnCode": [0,1],
    "failOnStderr": true
  }
}
```

### Expected Output Files
- `cpuTestOutput`: Contains metadata about the assigned CPU value.
- `memoryTestOutput`: Contains metadata about the assigned memory value.
- `retryTestOutput`: Confirms whether the retry mechanism worked as expected.
- `stderrTestOutput`: Confirms whether stderr handling matched the `failOnStderr` setting.

## Version
- **WDL Version**: 1.0

## Additional Notes
- This workflow demonstrates the correct application of runtime attributes in WDL.
- The `RetryTest` task intentionally fails intermittently to test retry behavior.
- The `StderrTest` task ensures stderr output handling is correctly enforced based on `options.json`.
- Tasks must generate their expected output files; missing files indicate failures in execution.



