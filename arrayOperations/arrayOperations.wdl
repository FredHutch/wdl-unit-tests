version 1.0
## This workflow tests array operations and scatter-gather functionality
## by converting an array of strings to uppercase.

#### WORKFLOW DEFINITION

workflow ArrayOperations {
    input {
        Array[String] strings
    }
    
    scatter (str in strings) {
        call Uppercase { input: text = str }
    }
    
    output {
        Array[String] uppercased = Uppercase.out
    }

    parameter_meta {
        strings: "Array of input strings to be converted to uppercase"
        uppercased: "Array of input strings converted to uppercase"
    }
}

#### TASK DEFINITIONS

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

    parameter_meta {
        text: "Input string to be converted to uppercase"
        out: "Input string converted to uppercase"
    }
}
