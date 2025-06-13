version 1.0

workflow testRemoteFileLocalization {
    input {
        String string
        Int integer
        Float float
        Boolean boolean
        File remote_file
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

    # Workflow outputs: include all outputs from all tasks
    output {
        File localized_file = testInputLocalization.processed_file
        File localized_string = testInputLocalization.outputStringfile
        File localized_integer = testInputLocalization.outputIntegerfile
        File localized_float = testInputLocalization.outputFloatfile
        File localized_boolean = testInputLocalization.outputBooleanfile
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

    String input_base_name = basename(input_file)

    command <<<
        # Generate and verify input-based outputs
        echo "~{input_string}" > localized_string.txt
        echo "~{input_integer}" > localized_integer.txt
        echo "~{input_float}" > localized_float.txt
        echo "~{input_boolean}" > localized_boolean.txt

        # Input file is expected to already be localized by WDL
        cp "~{input_file}" "~{input_base_name}"
    >>>

    output {
        File outputStringfile = "localized_string.txt"
        File outputIntegerfile = "localized_integer.txt"
        File outputFloatfile = "localized_float.txt"
        File outputBooleanfile = "localized_boolean.txt"
        File processed_file = "~{input_base_name}"
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
        mv ~{processed_file} renamed_file.txt
    >>>

    output {
        File renamed_file = "renamed_file.txt"
    }

    runtime {
        docker: "ubuntu:20.04"
    }
}
