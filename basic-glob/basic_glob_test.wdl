version 1.0

workflow basic_glob_test {
    call create_files
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
