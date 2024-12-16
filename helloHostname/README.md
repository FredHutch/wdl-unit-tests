# HelloHostname WDL Workflow

## Overview
A simple test workflow that demonstrates basic WDL functionality by returning the hostname of the compute node where the job is executed. This workflow is particularly useful for testing backend configurations and verifying proper job distribution.

## Workflow Components

### Workflow: `HelloHostname`
The main workflow executes a single task and returns its output.

**Outputs:**
- `stdout`: File containing the hostname of the execution node

### Task: `Hostname`
A basic task that executes the `hostname` command and captures its output.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB

**Outputs:**
- `out`: File containing the hostname of the execution node

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run helloHostname.wdl

# Execute with miniwdl
miniwdl run helloHostname.wdl
```

## Purpose
This workflow serves as a basic test case for:
- WDL execution environment validation
- Backend configuration verification
- Basic resource allocation testing
- Output handling validation

## Version
WDL 1.0
