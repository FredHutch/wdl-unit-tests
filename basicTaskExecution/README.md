# Basic Task Execution WDL Workflow

## Overview
A test workflow that demonstrates the execution of a simple task in WDL. The workflow passes a string input to a task that writes the string to a file, verifying input handling, basic task execution, and file output generation.

## Workflow Components

### Workflow: `basicTaskTest`
The main workflow calls a single task `simpleTask`, passing a string input and generating a file with the content of that string.

**Inputs:**
- `text`: String - The text to be written to the output file. (Default: `"Hello, World!"`)

**Outputs:**
- `outputFile`: File - A file named `output.txt` containing the input text.

### Task: `simpleTask`
Writes the provided input string to a file using the `echo` command.

**Runtime Requirements:**
- Docker: `ubuntu:20.04`

**Inputs:**
- `message`: String - The text to write to the file.

**Outputs:**
- `outputFile`: File - The resulting file containing the written message.

**Command:**
```bash
echo "${message}" > output.txt
```

### Example Output
The workflow generates a file `output.txt` with the following content:
```
Hello, World!
```

## Purpose
This workflow serves as a test case for:
- Basic task execution in WDL
- Input handling for tasks and workflows
- File output generation
- Verification of runtime environments (Docker-based)

## Version
WDL 1.0

## Notes
- The default Docker image used is `ubuntu:20.04`.
- This workflow is ideal for testing backend support for task execution, input propagation, and file outputs.
