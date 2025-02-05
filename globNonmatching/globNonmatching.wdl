version 1.0

workflow globNonmatching {
    call create_files
    output {
        Array[File] unmatched_files = create_files.unmatched_files
    }
}

task create_files {
    command <<<
        echo "Test file" > test.txt
    >>>
    output {
        Array[File] unmatched_files = glob("*.log")
    }
}
