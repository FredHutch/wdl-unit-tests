# ArrayOperations WDL Workflow

## Overview
A comprehensive test workflow that demonstrates array handling, scatter-gather functionality, and various array operations in WDL. The workflow performs multiple array tests including empty array handling, indexing, array functions, concatenation, and nested array processing, while maintaining its original uppercase conversion functionality.

## Workflow Components

### Workflow: `ArrayOperations`
The main workflow demonstrates various array operations and parallel processing capabilities.

**Inputs:**
- `strings`: Array[String] - Primary list of strings to be processed
- `additional_strings`: Array[String] - Secondary array for testing concatenation (optional, defaults to empty)
- `nested_arrays`: Array[Array[String]] - Array of arrays for testing nested operations (optional, defaults to empty)

**Outputs:**
- `uppercased`: Array[String] - List of input strings converted to uppercase
- `first_index`: Int? - First valid index of the input array (0)
- `last_index`: Int? - Last valid index of the input array
- `sorted_array`: Array[String] - Input array sorted alphabetically
- `processed_nested`: Array[Array[String]] - Processed nested arrays
- `concat_test_passed`: Boolean - Validation result of array concatenation
- `array_length`: Int - Length of the input array
- `flattened`: Array[String] - Flattened version of nested arrays

### Tasks

#### Task: `Uppercase`
Converts a single string to uppercase using the Unix `tr` command.

#### Task: `ValidateIndex`
Validates array indexing by returning first and last valid indices.

#### Task: `ArrayFunctions`
Tests various array operations including sorting, length calculation, and flattening.

#### Task: `ArrayConcat`
Tests array concatenation and validates the resulting length.

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
  nested_arrays='[["nested1", "nested2"], ["nested3", "nested4"]]'
```

Example inputs.json:
```json
{
  "ArrayOperations.strings": ["hello", "world", "test"],
  "ArrayOperations.additional_strings": ["foo", "bar"],
  "ArrayOperations.nested_arrays": [
    ["nested1", "nested2"],
    ["nested3", "nested4"]
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
- Scatter-gather operations
- Parallel task execution
- Basic string manipulation
- Output array collection

## Version
WDL 1.0

## Notes
- Useful for testing backend's ability to handle parallel task execution
- Demonstrates proper scatter-gather syntax
- Shows comprehensive array manipulation patterns
- Handles edge cases like empty arrays
- Tests multiple array operations in a single workflow
- Provides validation for array operations
