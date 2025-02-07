version 1.0

workflow WildcardsandConditions {
    input {
        String prefix  # Required input for the file prefix (no default value)
    }

    call wildcard_and_conditions_test {
        input:
            prefix = prefix  # Explicitly pass the workflow input to the task
    }

    output {
        Array[File] txt_files = wildcard_and_conditions_test.txt_files
        String conditional_result = wildcard_and_conditions_test.conditional_output
    }
}

task wildcard_and_conditions_test {
    input {
        String prefix  # Required input for file creation
        Boolean create_extra_file = true  # Default value for conditional logic
    }

    command <<<
        # Create multiple .txt files to test wildcard resolution
        for i in {1..3}; do
            echo "File content $i" > "~{prefix}_$i.txt"
        done

        # Create an extra file conditionally
        if [[ ~{create_extra_file} == "true" ]]; then
            echo "Extra file content" > ~{prefix}_extra.txt
        fi

        # Parse inputs directly in the command
        echo "Parsed prefix: ~{prefix}" > parsed_output.txt
    >>>

    output {
        Array[File] txt_files = glob("*.txt")  # Test wildcard resolution
        String conditional_output = read_string("parsed_output.txt")  # Verify input parsing
    }

    runtime {
        docker: "ubuntu:20.04"
    }
}
