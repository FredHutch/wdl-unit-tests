version 1.0

workflow testRemoteFileLocalization {
    input {
        String string = "Hello, WDL!"  # String input
        Int integer = 42               # Integer input
        Float float = 3.14             # Float input
        Boolean boolean = true         # Boolean input
        File remote_file               # Remote file input
    }

    # Task 1: Test input localization and processing
    call testInputLocalization {
        input:
            input_string = string,
            input_integer = integer,
            input_float = float,
            input_boolean = boolean,
            input_file = remote_file
    }

    # Task 2: Use output from Task 1 as input
    call testOutputUsage {
        input:
            processed_file = testInputLocalization.processed_file
    }

    output {
        File localized_file = testInputLocalization.processed_file
        File renamed_file = testOutputUsage.renamed_file
    }
}

task testInputLocalization {
    input {
        String input_string
        Int input_integer
        Float input_float
        Boolean input_boolean
        File input_file
    }

    command <<<
        # Verify localization of inputs and process them
        echo "${input_string}" > localized_string.txt
        echo "${input_integer}" > localized_integer.txt
        echo "${input_float}" > localized_float.txt
        echo "${input_boolean}" > localized_boolean.txt

        # Ensure the input_file exists and copy it
        if [[ -f "${input_file}" ]]; then
            cp "${input_file}" processed_file.txt
        else
            echo "Input file not found: ${input_file}" >&2
            exit 1
        fi
    >>>

    output {
        File processed_file = "processed_file.txt"
    }

    runtime {
        docker: "ubuntu:20.04"
    }
}

task testOutputUsage {
    input {
        File processed_file
    }

    command <<<
        # Rename the file received from the previous task
        mv ${processed_file} renamed_file.txt
    >>>

    output {
        File renamed_file = "renamed_file.txt"
    }

    runtime {
        docker: "ubuntu:20.04"
    }
}
