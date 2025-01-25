# HelloDockerHostname WDL Workflow

## Overview
A test workflow that validates Docker container execution in WDL by running commands within a specified container and verifying the container environment. The workflow confirms both the container image and version, while also capturing the hostname of the execution node.

## Workflow Components

### Workflow: `HelloDockerHostname`
The main workflow executes a task within a specified Docker container and validates the container environment.

**Inputs:**
- `docker_image`: String specifying the Docker image (default: "ubuntu:20.04")

**Outputs:**
- `stdout`: File containing container verification and hostname information

### Task: `Hostname`
Validates the Docker environment and executes commands within the container.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Docker: Configurable via input (defaults to ubuntu:latest)

**Validation Checks:**
- Verifies Docker image name matches expected value
- Confirms image version/tag matches specified version

## Usage
```bash
# Execute with default Ubuntu latest
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

## Purpose
- Docker container integration testing
- Container environment validation
- Image and version verification
- Resource allocation validation
- Backend Docker support verification

## Version
WDL 1.0
