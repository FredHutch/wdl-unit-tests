version 1.0

workflow basicGlobTest {
    call create_files
    
    if (length(create_files.txt_files) != 1) {
        call fail_workflow { 
            input: message = "Expected 2 txt files but found " + length(create_files.txt_files) 
        }
    }
    
    output {
        Array[File] matched_files = create_files.txt_files
    }
}

task create_files {
    command <<<
        echo "File 1" > file1.txt
        echo "File 2" > file2.txt
    >>>
    output {
        Array[File] txt_files = glob("*.txt")
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
