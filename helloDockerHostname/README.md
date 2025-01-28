# HelloDockerHostname WDL Workflow

## Overview
A test workflow that validates Docker container execution in WDL by running commands within a specified container and verifying the container environment. The workflow confirms both the container image and version, captures the hostname of the execution node, and measures task execution time with validation against a maximum duration threshold.

## Workflow Components

### Workflow: `HelloDockerHostname`
The main workflow executes a task within a specified Docker container, validates the container environment, and measures execution time.

**Inputs:**
- `docker_image`: String specifying the Docker image (default: "ubuntu:20.04")

**Outputs:**
- `stdout`: File containing container verification and hostname information
- `execution_time_seconds`: Float indicating the duration of the Hostname task execution
- `within_time_limit`: Boolean indicating whether execution completed within the 2-minute limit

### Tasks

#### Task: `Hostname`
Validates the Docker environment and executes commands within the container.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: Configurable via input (defaults to ubuntu:20.04)

**Validation Checks:**
- Verifies Docker image name matches expected value
- Confirms image version/tag matches specified version

#### Task: `GetStartTime`
Records the start time before Hostname task execution.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: ubuntu:20.04

#### Task: `GetEndTime`
Records the end time after Hostname task completion.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: ubuntu:20.04

#### Task: `ValidateExecutionTime`
Calculates execution duration and validates it against the 2-minute threshold.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: ubuntu:20.04

## Usage
```bash
# Execute with default Ubuntu 20.04
java -jar cromwell.jar run helloDockerHostname.wdl

# Execute with specific Docker image
java -jar cromwell.jar run helloDockerHostname.wdl -i inputs.json

# Using miniwdl with specific image
miniwdl run helloDockerHostname.wdl docker_image=ubuntu:20.04
```

Example inputs.json:
```json
{
  "HelloDockerHostname.docker_image": "ubuntu:20.04"
}
```

Example outputs:
```json
{
  "HelloDockerHostname.stdout": "File",
  "HelloDockerHostname.execution_time_seconds": 1.234,
  "HelloDockerHostname.within_time_limit": true
}
```

## Purpose
- Docker container integration testing
- Container environment validation
- Image and version verification
- Resource allocation validation
- Backend Docker support verification
- Task execution time measurement and validation
- Workflow dependency handling demonstration

## Version
WDL 1.0
