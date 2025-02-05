# GPU Allocation Test (GpuMatrixMult)

## Overview
The GpuMatrixMult workflow is a unit test designed to validate GPU allocation and basic tensor operations using TensorFlow. It serves as a verification tool to ensure that workflows can successfully request and utilize GPU resources in a WDL execution environment.

## Purpose
This workflow tests and validates:
- Proper GPU allocation in the runtime environment
- TensorFlow's ability to detect and utilize GPU resources
- Basic matrix multiplication operations using TensorFlow
- Docker container integration with GPU support
- Output handling of GPU computations

## Workflow Components

### Workflow: `GpuMatrixMult`
The main workflow orchestrates the GPU test and collects the results.

**Outputs:**
- `test_results`: File - Complete log of the GPU test execution
- `gpu_count`: Int - Number of GPUs detected by TensorFlow
- `matrix_result`: Array[Float] - Results of the matrix multiplication operation

### Task: `GpuTest`
Performs the actual GPU testing and tensor operations.

**Operations:**
1. Detects available GPUs
2. Creates test matrices
3. Performs matrix multiplication
4. Captures and formats results

**Runtime Requirements:**
- GPU: "1" (needs to be a string)
- Docker: tensorflow/tensorflow:latest-gpu

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run gpuAlloc.wdl

# Execute with miniwdl (if GPU support is configured)
miniwdl run gpuAlloc.wdl
```

## Expected Output
The workflow should produce:
1. A log file containing:
   - GPU detection information
   - Matrix multiplication results
   - TensorFlow execution details
2. The number of detected GPUs
3. The result of the matrix multiplication operation

## Verification
The workflow can be considered successful if:
1. It completes without errors
2. Reports at least one GPU detected
3. Successfully performs the matrix multiplication
4. All outputs are properly captured and formatted

## Requirements
- Runtime environment with GPU support
- Docker with GPU support (nvidia-docker)
- TensorFlow GPU-compatible environment
- Sufficient GPU memory for basic tensor operations

## Version
WDL 1.0

## Additional Notes
- Useful for verifying GPU support in new environments
- Can serve as a template for more complex GPU workflows
- Validates both resource allocation and computational correctness
- Demonstrates proper GPU resource specification in WDL
- Shows integration of TensorFlow with WDL workflows
