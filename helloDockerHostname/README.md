# HelloDockerHostname WDL Workflow

## Overview
A test workflow that demonstrates Docker container integration in WDL by returning the hostname of the compute node where the job is executed. This workflow extends the basic hostname test by running the command within a Docker container.

## Workflow Components

### Workflow: `HelloDockerHostname`
The main workflow executes a single task within a Docker container and returns its output.

**Outputs:**
- `stdout`: File containing the hostname of the execution node

### Task: `Hostname`
Executes the `hostname` command within an Ubuntu Docker container.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: `ubuntu:latest`

**Outputs:**
- `out`: File containing the hostname of the execution node

## Usage
```bash
# Execute with cromwell
java -jar cromwell.jar run helloDockerHostname.wdl

# Execute with miniwdl
miniwdl run helloDockerHostname.wdl
```

## Purpose
This workflow serves as a test case for:
- Docker container integration
- Container runtime environment validation
- Basic resource allocation testing
- Output handling validation from containerized tasks
- Backend Docker support verification

## Version
WDL 1.0

## Notes
- Comparing outputs between this and the non-Docker version can help verify proper container execution
