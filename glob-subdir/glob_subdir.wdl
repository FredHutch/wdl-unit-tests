workflow glob_subdirectory_test {
    call create_nested_files
    output {
        Array[File] matched_files = flatten([create_nested_files.matched_files_top, create_nested_files.matched_files_nested])
    }
}

task create_nested_files {
    command <<<
        mkdir -p subdir/nested
        echo "Hello" > subdir/nested/file1.txt
        echo "World" > subdir/file2.txt
    >>>
    output {
        Array[File] matched_files_top = glob("subdir/*.txt")
        Array[File] matched_files_nested = glob("subdir/**/*.txt")
    }
}
