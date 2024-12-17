# StructAndMapTypes WDL Workflow

## Overview
A test workflow that demonstrates the usage of struct and map types in WDL. The workflow processes user information stored in a struct and handles a map of test scores, showing how to work with complex data types in WDL.

## Workflow Components

### Struct Definition: `User`
Defines a custom struct type with the following fields:
- `name`: String
- `age`: Int
- `preferences`: Map[String, String]

### Workflow: `StructAndMapTypes`
The main workflow that processes a User struct and a map of scores.

**Inputs:**
- `user`: User struct containing user information
- `scores`: Map[String, Int] containing test scores

**Outputs:**
- `user_summary`: String containing processed user information
- `processed_scores`: Map[String, Int] containing processed scores

### Task: `ProcessUser`
Processes the user information and test scores, creating a summary.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run structAndMapTypes.wdl -i inputs.json

# Execute with miniwdl
miniwdl run structAndMapTypes.wdl user.name=John user.age=30 'user.preferences={"theme":"dark","language":"en"}' 'scores={"test1":95,"test2":87}'
```

Example inputs.json:
```json
{
  "StructAndMapTypes.user": {
    "name": "John",
    "age": 30,
    "preferences": {
      "theme": "dark",
      "language": "en"
    }
  },
  "StructAndMapTypes.scores": {
    "test1": 95,
    "test2": 87
  }
}
```

## Purpose
This workflow serves as a test case for:
- Struct type definition and usage
- Map type handling
- Complex input parsing
- Nested data structure processing
- Type checking and validation

## Version
WDL 1.0

## Notes
- Demonstrates proper struct definition syntax
- Shows map type usage with different value types
- Illustrates nested map handling within structs
- Tests input parsing for complex types
