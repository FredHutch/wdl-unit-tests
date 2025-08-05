version 1.0

workflow ArrayOperations {
    input {
        # Input arrays for different tests
        Array[String] strings
        Array[String] additional_strings = []  # For testing array concatenation
        Array[Array[String]] nested_arrays = []  # For testing nested arrays
        Array[Int] numbers = [1, 2, 3, 4, 5]  # Default integer array for numeric operations
        Array[File] input_files = [] # Array of files to test file operations
    }

    # Scatter operation to test processing of each element in an array
    # Test empty arrays (original operation still works with empty input)
    scatter (str in strings) {
        call Uppercase { input: text = str }
    }

    # Test array indexing (accessing first and last elements)
    if (length(strings) > 0) {
        call ValidateIndex { input: arr = strings }
    }

    # Test array functions like sorting, length calculation, and flattening
    call ArrayFunctions {
        input:
            arr = strings,
            nested = nested_arrays
    }

    # Test array concatenation and verify the combined length
    Array[String] combined = flatten([strings, additional_strings])
    call ArrayConcat {
        input:
            arr1 = strings,
            arr2 = additional_strings,
            expected_length = length(combined)
    }

    # Test integer array operations like summation and combining arrays
    Array[Int] more_numbers = [6, 7, 8, 9, 10]  # Intermediate array declaration
    call IntegerArrayOps {
        input:
            numbers = numbers,
            additional_numbers = more_numbers
    }

    # Test file array operations like localization and content reading
    if (length(input_files) > 0) {
        call FileArrayOps {
            input:
                files = input_files
        }
    }
    # Outputs to capture results of the tests
    output {
        Array[String] uppercased = Uppercase.out # Outputs from scatter task
        Int? first_index = ValidateIndex.first_index # First index in string array
        Int? last_index = ValidateIndex.last_index # Last index in string array
        Array[String] sorted_array = ArrayFunctions.sorted # Sorted array
        Array[Array[String]] processed_nested = ArrayFunctions.processed_nested # Processed nested array
        Boolean concat_test_passed = ArrayConcat.test_passed # Result of concatenation test
        Int array_length = ArrayFunctions.arr_length # Length of input array
        Array[String] flattened = ArrayFunctions.flattened # Flattened nested arrays
        # New outputs for integer array operations
        Int sum_result = IntegerArrayOps.sum # Sum of integer array
        Array[String] combined_numbers = IntegerArrayOps.combined # Combined integer arrays
        # New outputs for file array operations
        Array[String]? file_contents = FileArrayOps.contents # Contents of files
        Boolean? files_localized = FileArrayOps.localization_success # File localization status
    }

    parameter_meta {
        # Descriptions for inputs
        strings: "Primary array of input strings"
        additional_strings: "Secondary array for testing concatenation"
        nested_arrays: "Array of arrays for testing nested array operations"
        numbers: "Array of integers for testing numeric operations"
        input_files: "Array of input files for testing file localization"
    }
}

# Task to convert string to uppercase (tests per-element processing)
task Uppercase {
    input {
        String text
    }

    command <<<
        echo "~{text}" | tr '[:lower:]' '[:upper:]'
    >>>

    output {
        String out = read_string(stdout())
    }

    runtime {
        cpu: 1
        memory: "1 GB"
    }
}


# Task to test indexing operations
task ValidateIndex {
    input {
        Array[String] arr
    }

    command <<<
        echo "0" > first_index.txt  # First index
        echo "~{length(arr)-1}" > last_index.txt  # Last index
    >>>

    output {
        Int first_index = read_int("first_index.txt")
        Int last_index = read_int("last_index.txt")
    }

    runtime {
        cpu: 1
        memory: "1 GB"
    }
}

# Task to test array functions
task ArrayFunctions {
    input {
        Array[String] arr
        Array[Array[String]] nested
    }

    command <<<
        # Sort the input array using bash
        echo "~{sep='\n' arr}" | sort > sorted.txt

        # Get array length
        echo "~{length(arr)}" > length.txt

        # Process nested arrays (flatten them)
        echo "~{sep='\n' flatten(nested)}" > flattened.txt
    >>>

    output {
        Array[String] sorted = read_lines("sorted.txt")
        Int arr_length = read_int("length.txt")
        Array[String] flattened = read_lines("flattened.txt")
        Array[Array[String]] processed_nested = nested  # Return the original nested array
    }

    runtime {
        cpu: 1
        memory: "1 GB"
    }
}

# Task to test concatenation of two arrays
task ArrayConcat {
    input {
        Array[String] arr1
        Array[String] arr2
        Int expected_length
    }

    command <<<
        actual_length=$(( ~{length(arr1)} + ~{length(arr2)} ))
        if [ "$actual_length" -eq ~{expected_length} ]; then
            echo "true"
        else
            echo "false"
        fi
    >>>

    output {
        Boolean test_passed = read_boolean(stdout())
    }

    runtime {
        cpu: 1
        memory: "1 GB"
    }
}

# Task to test integer array operations
task IntegerArrayOps {
    input {
        Array[Int] numbers
        Array[Int] additional_numbers
    }

    command <<<
        # Calculate sum of numbers to verify proper parsing
        total=0
        for num in ~{sep=' ' numbers}; do
            total=$((total + num))
        done
        echo $total > sum.txt

        # Combine arrays and write to file
        echo "~{sep='\n' flatten([numbers, additional_numbers])}" > combined.txt
    >>>

    output {
        Int sum = read_int("sum.txt")
        Array[String] combined = read_lines("combined.txt")
    }

    runtime {
        cpu: 1
        memory: "1 GB"
    }
}

# Task to test file array operations
task FileArrayOps {
    input {
        Array[File] files
    }

    command <<<
        # Test file localization by reading contents
        for file in ~{sep=' ' files}; do
            if [ -f "$file" ]; then
                cat "$file" >> all_contents.txt
                echo "---" >> all_contents.txt  # Separator between files
            else
                echo "false" > localization_success.txt
                exit 1
            fi
        done
        echo "true" > localization_success.txt
    >>>

    output {
        Array[String] contents = read_lines("all_contents.txt")
        Boolean localization_success = read_boolean("localization_success.txt")
    }

    runtime {
        cpu: 1
        memory: "1 GB"
    }
}
