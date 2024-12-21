# Advanced Struct Types WDL Workflow

## Overview
A workflow that demonstrates advanced usage of struct types in WDL. The workflow processes sample information using nested structs and optional fields to organize metadata, showing how to define and work with complex structured data types in WDL.

## Workflow Components

### Struct Definitions

#### Struct: `SequencingInfo`
Defines the structure for sequencing metadata with the following fields:
- `platform`: String (required)
- `flowcell_id`: String (optional)
- `lane_number`: Int (optional)

#### Struct: `QualityMetrics`
Defines the structure for quality metrics with the following fields:
- `quality_score`: Float (required)
- `gc_content`: Float (optional)
- `duplicate_rate`: Int (optional)

#### Struct: `SampleInfo`
Main struct that demonstrates nested structures and optional fields:
- `name`: String (required)
- `type`: String (optional, defaults to "normal")
- `read_length`: Int (optional, defaults to 100)
- `library_prep`: String (optional, defaults to "Standard")
- `sequencing`: SequencingInfo (required, nested struct)
- `metrics`: QualityMetrics (required, nested struct)

### Workflow: `struct_example`
The main workflow that processes sample information using advanced struct types.

**Inputs:**
- `sample_information`: Array[SampleInfo] containing structured sample data with nested structs

**Process:**
- Scatters over the sample information array
- Applies default values for optional fields
- Processes each sample using the structured data

### Task: `process_sample`
Processes individual sample information using the complex struct types.

**Inputs:**
- `sample`: SampleInfo struct (includes nested structs)

**Outputs:**
- `message`: String containing processed sample information

**Runtime Requirements:**
- Docker: ubuntu:latest

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run structTypeTest.wdl -i inputs.json

# Execute with miniwdl
miniwdl run structTypeTest.wdl -i inputs.json
```

## Features Demonstrated
This workflow serves as a test case for:
- Complex struct type definitions and usage in WDL
- Nested struct implementation
- Optional fields with default values
- Array of structs handling
- Accessing nested struct members
- Default value handling using select_first()
- Docker container usage

## Advanced Features
The workflow demonstrates several advanced struct capabilities:
1. **Optional Fields**: Uses the `?` suffix to mark fields as optional
2. **Nested Structs**: Shows how to embed one struct within another
3. **Default Values**: Implements default values using `select_first()` in the workflow
4. **Complex Data Structures**: Demonstrates handling of multi-level structured data
5. **Robust Error Handling**: Includes fallback values for optional fields

## Version
WDL 1.0

## Notes
- Demonstrates proper nested struct type definition
- Shows how to handle optional fields with defaults
- Illustrates accessing nested struct members in command blocks
- Tests input parsing for complex struct types
- Provides examples of proper error handling for optional fields
- Includes comprehensive input validation
