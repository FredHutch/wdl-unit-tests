# ArrayOperations WDL Workflow

## Overview
A comprehensive test workflow that demonstrates array handling, scatter-gather functionality, and various array operations in WDL. The workflow performs multiple array tests including empty array handling, indexing, array functions, concatenation, nested array processing, integer array operations, and file array localization, while maintaining its original uppercase conversion functionality.

## Workflow Components

### Workflow: `ArrayOperations`
The main workflow demonstrates various array operations and parallel processing capabilities.

**Inputs:**
- `strings`: Array[String] - Primary list of strings to be processed
- `additional_strings`: Array[String] - Secondary array for testing concatenation (optional, defaults to empty)
- `nested_arrays`: Array[Array[String]] - Array of arrays for testing nested operations (optional, defaults to empty)
- `numbers`: Array[Int] - Array of integers for testing numeric operations (optional, defaults to [1,2,3,4,5])
- `input_files`: Array[File] - Array of input files for testing file localization (optional, defaults to empty)

**Outputs:**
- `uppercased`: Array[String] - List of input strings converted to uppercase
- `first_index`: Int? - First valid index of the input array (0)
- `last_index`: Int? - Last valid index of the input array
- `sorted_array`: Array[String] - Input array sorted alphabetically
- `processed_nested`: Array[Array[String]] - Processed nested arrays
- `concat_test_passed`: Boolean - Validation result of array concatenation
- `array_length`: Int - Length of the input array
- `flattened`: Array[String] - Flattened version of nested arrays
- `sum_result`: Int - Sum of the input integer array (verifies proper parsing)
- `combined_numbers`: Array[Int] - Combined array of input and intermediate integers
- `file_contents`: Array[String]? - Contents of the localized files
- `files_localized`: Boolean? - Success status of file localization

### Tasks

#### Task: `Uppercase`
Converts a single string to uppercase using the Unix `tr` command.

#### Task: `ValidateIndex`
Validates array indexing by returning first and last valid indices.

#### Task: `ArrayFunctions`
Tests various array operations including sorting, length calculation, and flattening.

#### Task: `ArrayConcat`
Tests array concatenation and validates the resulting length.

#### Task: `IntegerArrayOps`
Tests integer array operations including summation and array combination.

#### Task: `FileArrayOps`
Tests file array localization and content access.

**Runtime Requirements:**
All tasks:
- CPU: 1 core
- Memory: 1 GB

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run arrayOperations.wdl -i inputs.json

# Execute with miniwdl
miniwdl run arrayOperations.wdl \
  strings='["hello", "world", "test"]' \
  additional_strings='["foo", "bar"]' \
  nested_arrays='[["nested1", "nested2"], ["nested3", "nested4"]]' \
  numbers='[1, 2, 3, 4, 5]' \
  input_files='["test1.txt", "test2.txt"]'
```

Example inputs.json:
```json
{
  "ArrayOperations.strings": ["hello", "world", "test"],
  "ArrayOperations.additional_strings": ["foo", "bar"],
  "ArrayOperations.nested_arrays": [
    ["nested1", "nested2"],
    ["nested3", "nested4"]
  ],
  "ArrayOperations.numbers": [1, 2, 3, 4, 5],
  "ArrayOperations.input_files": [
    "test1.txt",
    "test2.txt",
    "test3.txt"
  ]
}
```

## Purpose
This workflow serves as a comprehensive test case for:
- Array input/output handling
- Empty array processing
- Array indexing and bounds checking
- Array sorting and length calculations
- Array concatenation
- Nested array operations
- Integer array operations and parsing
- File array localization and access
- Scatter-gather operations
- Parallel task execution
- Basic string manipulation
- Output array collection
- Intermediate array declarations

## Version
WDL 1.0

## Notes
- Useful for testing backend's ability to handle parallel task execution
- Demonstrates proper scatter-gather syntax
- Shows comprehensive array manipulation patterns
- Handles edge cases like empty arrays
- Tests multiple array operations in a single workflow
- Provides validation for array operations
- Verifies proper integer parsing through arithmetic operations
- Tests file localization and accessibility in array context
- Demonstrates intermediate array declarations and manipulations
