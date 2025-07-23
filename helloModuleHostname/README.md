# HelloModuleHostname WDL Workflow

## Overview
A test workflow that demonstrates environment module integration in WDL by returning the hostname of the compute node where the job is executed. This workflow extends the basic hostname test by running the command within a specific module environment.

## Workflow Components

### Workflow: `HelloDockerHostname`
The main workflow executes a single task within a module-configured environment and returns its output.

**Outputs:**
- `stdout`: File containing the hostname of the execution node
- `module_loaded`: Boolean indicating if the specified module was successfully loaded

### Task: `Hostname`
Executes the `hostname` command within an environment with Python modules loaded.

**Runtime Requirements:**
- CPU: 1 core
- Memory: 1 GB
- Modules: Python/3.7.4-foss-2019b-fh1

**Outputs:**
- `out`: File containing the hostname of the execution node
- `module_verified`: Boolean indicating whether the module was successfully loaded

## Usage
Since the `modules` runtime parameter is specific to PROOF infrastructure, this workflow is best executed on the Fred Hutch HPC using PROOF rather than via the command line directly.

## Purpose
This workflow serves as a test case for:
- Environment module integration
- Module loading validation
- Basic resource allocation testing
- Output handling validation from module-enabled tasks
- Backend module support verification

## Version
WDL 1.0

## Notes
- Useful for testing HPC environments that use the module system for software management
