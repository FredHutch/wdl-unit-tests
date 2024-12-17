version 1.0
# This WDL workflow, required_inputs_test, is testing two things:
# String Validation: It checks whether the provided required_string is a non-empty string containing only alphabetic characters and spaces. If the string is invalid, the task will output an error message.
# Integer Validation: It checks whether the provided required_int is a valid integer (i.e., it contains only digits). If the integer is invalid, the task will output an error message.

workflow required_inputs_test {
    input {
        String required_string
        Int required_int
    }

    call validate_inputs {
        input:
            required_string = required_string,
            required_int = required_int
    }

    output {
        String output_message = read_string(validate_inputs.outputFile)
    }
}

task validate_inputs {
    input {
        String required_string
        Int required_int
    }

    command {
        # Check if required_string is a valid non-empty string (basic check for alphabetic input)
        if [[ -z "${required_string}" || ! "${required_string}" =~ ^[a-zA-Z[:space:]]*$ ]]; then
            echo "Invalid string input: ${required_string}" > output.txt
            exit 1
        fi

        # Check if required_int is a valid integer
        if ! [[ "${required_int}" =~ ^[0-9]+$ ]]; then
            echo "Invalid integer input: ${required_int}" > output.txt
            exit 1
        fi

        # If both checks pass, write success message to output.txt
        echo "Received required_string: ${required_string}" > output.txt
        echo "Received required_int: ${required_int}" >> output.txt
        echo "Validation successful!" >> output.txt
    }

    output {
        File outputFile = "output.txt"
    }

    runtime {
        docker: "ubuntu:20.04"
    }
}
