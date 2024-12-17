# Struct Types WDL Workflow

## Overview
A workflow that demonstrates the usage of struct types in WDL. The workflow processes sample information using a custom struct to organize metadata, showing how to define and work with structured data types in WDL.

## Workflow Components

### Struct: `SampleInfo`
Defines the structure for sample information with the following fields:
- `name`: String
- `type`: String
- `read_length`: Int
- `quality_score`: Float

### Workflow: `struct_example`
The main workflow that processes sample information using struct types.

**Inputs:**
- `sample_names`: Array[String] containing sample names
- `sample_information`: Array[SampleInfo] containing structured sample data

**Process:**
- Scatters over the sample information array
- Processes each sample using the structured data

### Task: `process_sample`
Processes individual sample information using the struct type.

**Inputs:**
- `sample`: SampleInfo struct

**Outputs:**
- `message`: String containing processed sample information

**Runtime Requirements:**
- Docker: ubuntu:latest

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run structTypeTest.wdl -i inputs.json

# Execute with miniwdl
miniwdl run structTypeTest.wdl
```

## Purpose
This workflow serves as a test case for:
- Struct type definition and usage in WDL
- Array of structs handling
- Accessing struct members
- Basic sample data processing
- Docker container usage

## Version
WDL 1.0

## Notes
- Demonstrates proper struct type definition
- Shows how to create and use arrays of structs
- Illustrates accessing struct members in command blocks
- Tests input parsing for struct types
