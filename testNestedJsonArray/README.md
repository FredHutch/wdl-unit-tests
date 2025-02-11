# Unit Test for Nested JSON Parsing in WDL (testNestedJsonArray)

## Overview

The `testNestedJsonArray` workflow is a unit test designed to validate the behavior of nested JSON parsing in WDL (Workflow Description Language). It tests the following:

- **Nested JSON Parsing**: Ensures that the nested JSON structure (e.g., an array of sample objects containing another nested object for details) is correctly parsed and passed to the workflow tasks.
- **Scatter Operation**: Verifies that the workflow can handle arrays of objects and correctly applies tasks to each object in the array.
- **File Output Generation**: Confirms that each sample's data is processed and written to a separate output file.

## Purpose

This workflow serves as a test case for:
- Parsing complex, nested JSON structures in WDL.
- Correctly processing an array of objects with nested fields.
- Using a scatter operation to process multiple objects in a workflow.
- Generating output files based on each sample's data.

## Workflow Components

### Workflow: `testNestedJsonArray`

This workflow demonstrates how nested JSON data can be parsed and processed using WDL, with a scatter operation to handle multiple samples.

**Inputs:**
- `cellNumber`: String - The number of cells in the experiment (required).
- `batchOfSamples`: Array[singleSample] - An array of sample objects, each containing detailed information about the sample (required).

**Outputs:**
- `result_allSampleInfo`: Array[File] - A list of output `.txt` files containing the formatted sample information.

### Tasks

#### Task: `processSample`
- **Purpose**: Processes each sample in the array, extracts the necessary details, formats the sample information into a string, and writes it to a `.txt` file.
- **Key Operations**:
  - Extracts sample details such as `sampleName`, `aboutSample`, `sampleDescription`, and details from the nested `details` object.
  - Formats the extracted information into a single string.
  - Writes the formatted string to a `.txt` file with the sample name as part of the filename.

**Runtime Requirements:**
- **Docker Image**: `ubuntu:latest`
- **CPU**: 1 core
- **Memory**: 1 GB

---
### Input JSON

To run the workflow, you need to specify the required `batchOfSamples` input in an `inputs.json` file. Here's an example:

```json
{
  "testNestedJsonArray.cellNumber": "10000",
  "testNestedJsonArray.batchOfSamples": [
    {
      "sampleName": "Sample1",
      "aboutSample": "This is sample 1",
      "sampleDescription": "Description of sample 1: A detailed description of the first sample.",
      "details": {
        "experimentType": "RNA-Seq",
        "prepMethod": "TruSeq",
        "tissueType": "blood"
      }
    },
    {
      "sampleName": "Sample2",
      "aboutSample": "This is sample 2",
      "sampleDescription": "Description of sample 2: A detailed description of the second sample.",
      "details": {
        "experimentType": "DNA-Seq",
        "prepMethod": "Nextera",
        "tissueType": "tissue biopsy"
      }
    },
    {
      "sampleName": "Sample3",
      "aboutSample": "This is sample 3",
      "sampleDescription": "Description of sample 3: A detailed description of the third sample.",
      "details": {
        "experimentType": "ChIP-Seq",
        "prepMethod": "Epigenome",
        "tissueType": "brain"
      }
    }
  ]
}
```

### Expected Output Files

1. **result_allSampleInfo**: This output will contain a list of `.txt` files, each corresponding to a sample. The files will be named based on the sample name (e.g., `Sample1.allSampleInfo.txt`), and will contain the formatted information about the sample.

   Example contents of output files:
   - `Sample1.allSampleInfo.txt`: `"Sample1 | This is sample 1 | Description of sample 1: A detailed description of the first sample. | RNA-Seq | TruSeq | blood"`
   - `Sample2.allSampleInfo.txt`: `"Sample2 | This is sample 2 | Description of sample 2: A detailed description of the second sample. | DNA-Seq | Nextera | tissue biopsy"`
   - `Sample3.allSampleInfo.txt`: `"Sample3 | This is sample 3 | Description of sample 3: A detailed description of the third sample. | ChIP-Seq | Epigenome | brain"`

---

## Version
- **WDL Version**: 1.0

---

## Additional Notes
- This workflow demonstrates how to parse and process nested JSON objects in WDL, specifically handling an array of objects with nested structures.
- The workflow uses a `scatter` operation to iterate over the array of sample objects and process each one individually, generating separate output files for each sample.
- If no value for `batchOfSamples` is provided, the workflow will fail with an error message, as the input is required.
