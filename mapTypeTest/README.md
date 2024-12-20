# Map Types WDL Workflow

## Overview
A comprehensive workflow that demonstrates advanced usage of map types in WDL. The workflow processes sample data including sample types (normal/tumor), read lengths, and nested patient information, showcasing various map operations and edge cases in WDL.

## Workflow Components

### Workflow: `enhanced_map_test`
The main workflow that demonstrates various map operations and edge cases.

**Inputs:**
- `samples`: Array[String] containing sample names
- `sample_metadata`: Map[String, String] mapping samples to their types (normal/tumor)
- `read_lengths`: Map[String, Int] mapping samples to their read lengths
- `empty_map`: Map[String, String] for testing empty map handling
- `nested_map`: Map[String, Map[String, String]] containing nested patient and sample information
- `patient_ids`: Array[String] containing patient identifiers for nested map processing

**Process:**
- Tests empty map processing
- Handles nested map structures for patient/sample relationships
- Scatters over sample array for basic map operations
- Generates result maps from processing outputs

### Tasks:

#### `process_empty_map`
Tests handling of empty maps.

**Inputs:**
- `empty_map`: Map[String, String]

**Outputs:**
- `success`: Boolean indicating if empty map was processed correctly

#### `process_nested_map`
Processes nested map structures containing patient and sample information.

**Inputs:**
- `patient_id`: String
- `patient_data`: Map[String, String]
- `samples_for_patient`: Array[String]

**Outputs:**
- `message`: String containing processed nested map information

#### `process_sample`
Processes individual sample information.

**Inputs:**
- `sample_name`: String
- `sample_type`: String (normal/tumor)
- `read_length`: Int

**Outputs:**
- `message`: String containing processed sample information

#### `create_result_map`
Aggregates processing results into a map structure.

**Inputs:**
- `sample_names`: Array[String]
- `processing_messages`: Array[String]

**Outputs:**
- `output_map`: Map[String, String] containing sample processing results

**Runtime Requirements:**
All tasks use Docker containers:
- `process_sample`, `process_empty_map`, `process_nested_map`: ubuntu:latest
- `create_result_map`: python:3.8-slim

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run enhanced_map_test.wdl -i inputs.json

# Execute with miniwdl
miniwdl run enhanced_map_test.wdl -i inputs.json
```

Example inputs.json:
```json
{
    "enhanced_map_test.samples": ["sample1", "sample2", "sample3"],
    "enhanced_map_test.sample_metadata": {
        "sample1": "normal",
        "sample2": "tumor",
        "sample3": "normal"
    },
    "enhanced_map_test.read_lengths": {
        "sample1": 100,
        "sample2": 150,
        "sample3": 100
    },
    "enhanced_map_test.empty_map": {},
    "enhanced_map_test.nested_map": {
        "patient1": {
            "sample1": "normal",
            "sample2": "tumor"
        },
        "patient2": {
            "sample3": "normal",
            "sample4": "tumor"
        }
    },
    "enhanced_map_test.patient_ids": ["patient1", "patient2"]
}
```

## Purpose
This workflow serves as a comprehensive test case for:
- Basic map operations in WDL
- Empty map handling
- Nested map structures
- Map output generation
- Array scattering with map lookups
- Docker container usage
- Map to array conversion techniques

## Version
WDL 1.0

## Notes
- Demonstrates proper map type usage and common patterns
- Shows how to access map values using array elements as keys
- Illustrates handling of empty maps
- Examples of nested map processing
- Demonstrates map output generation
- Provides workarounds for WDL 1.0 limitations (e.g., no built-in keys() function)
- Shows proper error handling for map operations