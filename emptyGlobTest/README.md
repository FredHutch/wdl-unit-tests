## **Overview**
This WDL workflow demonstrates how to use the `glob` function in WDL version 1.0 to collect files within a directory. The workflow creates an empty directory and attempts to collect `.txt` files from it. Since no `.txt` files are generated, the workflow will return an empty array, which showcases the behavior when no matching files are found.

## **Workflow Components**

### **Workflow: `emptyGlobTest`**
The main workflow calls the `create_empty_directory` task and then uses the `glob` function to collect any `.txt` files from the directory. In this case, as the directory is empty of `.txt` files, the result will be an empty array.

#### **Inputs:**
- None

#### **Outputs:**
- `no_files`: Array[File] - This will be an empty array as there are no `.txt` files in the directory.

### **Task: `create_empty_directory`**
This task creates an empty directory `empty_dir`. The task then attempts to collect any `.txt` files within the directory using the `glob` function.

#### **Runtime Requirements:**
- No special runtime requirements.

## **Purpose**
This workflow serves as a simple test case for demonstrating:
- The use of the `glob` function to collect files from a directory in WDL.
- How to handle cases where no files match the specified pattern (resulting in an empty array).

## **Version**
- WDL version: 1.0

## **Notes**
- This workflow demonstrates the basic usage of `glob` within a task in WDL v1.0.
- The workflow is expected to return an empty array for the `no_files` output because there are no `.txt` files in the created directory.
