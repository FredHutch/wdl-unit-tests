version 1.0

workflow ArrayOperations {
    input {
        Array[String] strings
        Array[String] additional_strings = []  # For testing array concatenation
        Array[Array[String]] nested_arrays = []  # For testing array of arrays
    }
    
    # Test empty arrays (original operation still works with empty input)
    scatter (str in strings) {
        call Uppercase { input: text = str }
    }
    
    # Test array indexing
    if (length(strings) > 0) {
        call ValidateIndex { input: arr = strings }
    }
    
    # Test array functions
    call ArrayFunctions { 
        input: 
            arr = strings,
            nested = nested_arrays
    }
    
    # Test array concatenation
    Array[String] combined = flatten([strings, additional_strings])
    call ArrayConcat {
        input: 
            arr1 = strings,
            arr2 = additional_strings,
            expected_length = length(combined)
    }
    
    output {
        Array[String] uppercased = Uppercase.out
        Int? first_index = ValidateIndex.first_index
        Int? last_index = ValidateIndex.last_index
        Array[String] sorted_array = ArrayFunctions.sorted
        Array[Array[String]] processed_nested = ArrayFunctions.processed_nested
        Boolean concat_test_passed = ArrayConcat.test_passed
        Int array_length = ArrayFunctions.arr_length
        Array[String] flattened = ArrayFunctions.flattened
    }

    parameter_meta {
        strings: "Primary array of input strings"
        additional_strings: "Secondary array for testing concatenation"
        nested_arrays: "Array of arrays for testing nested array operations"
    }
}

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
