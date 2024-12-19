# Map Types WDL Workflow

## Overview
A workflow that demonstrates the usage of map types in WDL. The workflow processes sample data including sample types (normal/tumor) and read lengths, showing how to work with map data types and array scattering in WDL.

## Workflow Components

### Workflow: `map_example`
The main workflow that processes sample information using maps for metadata and read lengths.

**Inputs:**
- `samples`: Array[String] containing sample names
- `sample_metadata`: Map[String, String] mapping samples to their types (normal/tumor)
- `read_lengths`: Map[String, Int] mapping samples to their read lengths

**Process:**
- Scatters over the sample array
- For each sample, looks up corresponding metadata and read length from maps
- Processes each sample with the retrieved information

### Task: `process_sample`
Processes individual sample information.

**Inputs:**
- `sample_name`: String
- `sample_type`: String (normal/tumor)
- `read_length`: Int

**Outputs:**
- `message`: String containing processed sample information

**Runtime Requirements:**
- Docker: ubuntu:latest

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run structAndMapTypes.wdl -i inputs.json

# Execute with miniwdl
miniwdl run structAndMapTypes.wdl
```

Example inputs.json:
```json
{
    "map_example.samples": ["sample1", "sample2", "sample3"],
    "map_example.sample_metadata": {
        "sample1": "normal",
        "sample2": "tumor",
        "sample3": "normal"
    },
    "map_example.read_lengths": {
        "sample1": 100,
        "sample2": 150,
        "sample3": 100
    }
}
```

## Purpose
This workflow serves as a test case for:
- Map type handling in WDL
- Array scattering with map lookups
- Basic sample data processing
- Docker container usage

## Version
WDL 1.0

## Notes
- Demonstrates proper map type usage
- Shows how to access map values using array elements as keys
- Illustrates basic scatter operation over an array
- Tests input parsing for map types
