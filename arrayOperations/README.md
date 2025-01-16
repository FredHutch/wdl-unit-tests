# Unit test for Array Operations (ArrayOperations)

## Overview
The ArrayOperations workflow is a unit test designed to validate and demonstrate various operations on arrays in WDL (Workflow Description Language). It includes tests for:

- String Arrays: Manipulations like uppercase conversion, indexing, sorting, concatenation, and flattening.
- Integer Arrays: Operations like summation and concatenation.
- Nested Arrays: Flattening and validation.
- File Arrays: Localization and content reading.
- Edge cases : Empty arrays 

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

## Workflow Components

### Workflow: `ArrayOperations`
The main workflow demonstrates various array operations and parallel processing capabilities.

**Inputs:**
- `strings`: Array[String] - Primary array of input strings for testing.
- `additional_strings`: Array[String] - Secondary array for testing concatenation (optional, defaults to empty)
- `nested_arrays`: Array[Array[String]] - Array of arrays for testing flattening and nested operations (optional, defaults to empty)
- `numbers`: Array[Int] - Array of integers for testing numeric operations (optional, defaults to [1,2,3,4,5])
- `input_files`: Array[File] - Array of input files for testing file localization (optional, defaults to empty)

**Outputs:**
- `uppercased`: Array[String] - Uppercased elements from the input string array.
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
  input_files='["data/test1.txt", "data/test2.txt"]'
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
    "data/test1.txt",
    "data/test2.txt",
    "data/test3.txt"
  ]
}
```

## Version
WDL 1.0

## Additional Notes
- Useful for testing backend's ability to handle parallel task execution
- Demonstrates proper scatter-gather syntax
- Shows comprehensive array manipulation patterns
- Handles edge cases like empty arrays
- Tests multiple array operations in a single workflow
- Provides validation for array operations
- Verifies proper integer parsing through arithmetic operations
- Tests file localization and accessibility in array context
- Demonstrates intermediate array declarations and manipulations
