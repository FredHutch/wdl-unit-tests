# `basic_glob_test` WDL Workflow

## **Overview**
This workflow demonstrates the use of the `glob` function to collect multiple `.txt` files created by a task. The workflow ensures that all matching files are gathered as outputs.

---

## **Workflow Components**

### **Workflow: `basic_glob_test`**
The workflow calls a task to create `.txt` files and gathers them using the `glob` function.

**Outputs**:
- `matched_files`: `Array[File]` - List of `.txt` files created by the task.

### **Task: `create_files`**
The task generates two sample `.txt` files and collects all `.txt` files in the working directory using `glob`.

---

### **Expected Output**

The task `create_files` generates:
- `file1.txt`
- `file2.txt`

The `glob` function collects these files into an `Array[File]`:
```json
{
  "basic_glob_test.matched_files": ["file1.txt", "file2.txt"]
}
```

---

## **Purpose**
This workflow serves as a test case for:
- Correct use of `glob` in WDL tasks
- Collecting multiple output files dynamically
- Demonstrating file handling and task outputs in WDL

---

## **Version**
WDL 1.0

---

## **Notes**
- The `glob` function must be used **inside a task**, not directly in workflow outputs.
