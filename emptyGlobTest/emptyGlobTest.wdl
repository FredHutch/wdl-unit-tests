version 1.0

workflow emptyGlobTest {
    call create_empty_directory
    
    if (length(create_empty_directory.no_files) != 0) {
        call fail_workflow { 
            input: message = "Expected 0 txt files but found " + length(create_empty_directory.no_files)
        }
    }

    output {
        Array[File] no_files = create_empty_directory.no_files
    }
}

task create_empty_directory {
    command {
        mkdir empty_dir
    }
    output {
        Array[File] no_files = glob("empty_dir/*.txt")
    }
}

task fail_workflow {
    input {
        String message
    }
    command {
        set -eo pipefail
        echo "~{message}"
        exit 1
    }
    output {
        String out = read_string(stdout())
    }
}
