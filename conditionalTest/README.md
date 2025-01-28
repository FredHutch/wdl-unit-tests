# Conditional Statements WDL Workflow

## Overview
A workflow that demonstrates the usage of conditional statements in WDL. The workflow processes sample information using structs and demonstrates different types of conditional operations including if statements in scatter blocks and mutually exclusive conditional blocks.

## Workflow Components

### Struct: `SampleInfo`
Defines the structure for sample information with the following fields:
- `name`: String
- `quality_score`: Float
- `type`: String

### Workflow: `conditional_example`
The main workflow that demonstrates various conditional operations.

**Inputs:**
- `samples`: Array[SampleInfo] containing structured sample data
- `quality_threshold`: Float threshold for high-quality samples

**Outputs:**
- `final_summary`: String containing the processing summary
- `qc_report`: File containing detailed QC information for all samples

**Conditional Operations Demonstrated:**
1. If statement within scatter (processing high-quality samples)
2. Multiple mutually exclusive conditional blocks (WDL 1.0 style branching)
3. Usage of select_all() with conditional outputs
4. Usage of select_first() for mutually exclusive task outputs

### Tasks:
1. `process_high_quality`: Processes samples that meet quality threshold
2. `run_qc_report`: Generates QC report for all samples
3. `summarize`: Creates summary based on number of processed samples

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run conditionalTest.wdl -i inputs.json

# Execute with miniwdl
miniwdl run conditionalTest.wdl -i inputs.json
```

## Purpose
This workflow serves as a test case for:
- Conditional execution in WDL 1.0
- If statements within scatter blocks
- Mutually exclusive conditional blocks
- Handling optional outputs with select_all()
- Accessing struct members
- Basic sample data processing
- Docker container usage

## Version
WDL 1.0

## Notes
- Demonstrates proper conditional statement usage in WDL 1.0
- Shows how to handle mutually exclusive execution paths
- Illustrates conditional logic within scatter blocks
- Shows proper struct member access
- Tests input parsing for struct types
