
# `symlinkOnly` WDL Workflow

## **Overview**
This workflow demonstrates the handling of symbolic links in WDL tasks. It creates a symbolic link to a text file and captures the symlink as a task output.

## **Workflow Components**

### **Workflow: `symlinkOnly`**
The workflow consists of a single task that creates and returns a symbolic link.

**Outputs**:
- `symlink_file`: `File` - A symbolic link to a text file created in the task.

### **Task: `generate_diverse_outputs`**
This task:
- Creates a regular text file (`original.txt`)
- Creates a symbolic link to it (`link.txt`)
- Outputs the symlink as `symlink_output`

The task runs in a minimal Ubuntu Docker container for a clean and reproducible environment.



## **Expected Output**

The task `generate_diverse_outputs` generates:
- `original.txt`
- `link.txt` (a symbolic link to `original.txt`)

The workflow collects the symlink as output:
```json
{
  "symlinkOnly.symlink_file": "link.txt"
}
```


## **Purpose**
This workflow serves as a test case for:
- Creating and outputting symbolic links in WDL
- Validating behavior of symlinks as outputs
- Testing runtime behavior in containerized environments



## **Version**
WDL 1.0


