# `globSymlink` WDL Workflow

## **Overview**
This workflow is designed to test how the `glob` function behaves when used to collect files that include symbolic links. It validates that symlinked `.txt` files can be successfully matched and returned as task outputs alongside regular files.



## **Workflow Components**

### **Workflow: `globSymlink`**
The workflow calls a single task to generate `.txt` files and symlinks, and gathers matching files using the `glob` function.

**Outputs**:
- `matched_files`: `Array[File]` – A flattened list of `.txt` files matched using two `glob` patterns:
  - Top-level files in `subdir/`
  - Nested `.txt` files in `subdir/**/`
- `symlink_matches`: `Array[File]` – `.txt` files matched from the `symlinks/` directory (symlinks pointing to actual files)



### **Task: `create_nested_files`**
This task:
- Creates two `.txt` files:
  - `subdir/nested/file1.txt`
  - `subdir/file2.txt`
- Creates a `symlinks/` directory and adds symbolic links pointing to the `.txt` files above:
  - `symlinks/link_to_file1.txt` → `subdir/nested/file1.txt`
  - `symlinks/link_to_file2.txt` → `subdir/file2.txt`

**Glob Outputs**:
- `matched_files_top`: Files matched in `subdir/*.txt`
- `matched_files_nested`: Files matched in `subdir/**/*.txt`
- `matched_symlinks`: Files matched in `symlinks/*.txt` (symbolic links)



## **Expected Output**
```json
{
  "globSymlink.matched_files": [
    "subdir/file2.txt",
    "subdir/nested/file1.txt"
  ],
  "globSymlink.symlink_matches": [
    "symlinks/link_to_file1.txt",
    "symlinks/link_to_file2.txt"
  ]
}
```



## **Purpose**
This unit test serves to validate:
- Proper use of `glob` for collecting nested and symlinked files
- That symbolic links are treated as valid file matches by `glob`
- Compatibility of file collection patterns with Cromwell’s runtime



## **Version**
WDL 1.0


## **Runtime Options**
**`options.json`:**
```json
{
  "workflow_failure_mode": "ContinueWhilePossible",
  "write_to_cache": false,
  "read_from_cache": false
}
```

These settings disable call caching and ensure the workflow continues executing even if a task fails, supporting robust unit test evaluation.
