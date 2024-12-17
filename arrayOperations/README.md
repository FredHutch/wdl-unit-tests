# ArrayOperations WDL Workflow

## Overview
A test workflow that demonstrates array handling and scatter-gather functionality in WDL. The workflow takes an array of strings and converts each element to uppercase, demonstrating parallel processing capabilities and array input/output handling.

## Workflow Components

### Workflow: `ArrayOperations`
The main workflow scatters over an input array, processes each element independently, and gathers the results.

**Inputs:**
- `strings`: Array[String] - List of strings to be processed

**Outputs:**
- `uppercased`: Array[String] - List of input strings converted to uppercase

### Task: `Uppercase`
Converts a single string to uppercase using the Unix `tr` command.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB

**Inputs:**
- `text`: String - Input string to be converted

**Outputs:**
- `out`: String - Uppercase version of the input string

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run arrayOperations.wdl -i inputs.json

# Execute with miniwdl
miniwdl run arrayOperations.wdl strings='["hello", "world", "test"]'
```

Example inputs.json:
```json
{
  "ArrayOperations.strings": ["hello", "world", "test"]
}
```

## Purpose
This workflow serves as a test case for:
- Array input/output handling
- Scatter-gather operations
- Parallel task execution
- Basic string manipulation
- Output array collection

## Version
WDL 1.0

## Notes
- Useful for testing backend's ability to handle parallel task execution
- Demonstrates proper scatter-gather syntax
- Shows basic array manipulation patterns
