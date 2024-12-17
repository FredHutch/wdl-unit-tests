version 1.0

workflow empty_glob_test {
    call create_empty_directory

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
