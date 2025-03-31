version 1.0

workflow globSymlink {
    call create_nested_files
    output {
        Array[File] matched_files = flatten([create_nested_files.matched_files_top, create_nested_files.matched_files_nested])
        Array[File] symlink_matches = create_nested_files.matched_symlinks
    }
}

task create_nested_files {
    command <<<
        mkdir -p subdir/nested
        echo "Hello" > subdir/nested/file1.txt
        echo "World" > subdir/file2.txt

        # Create symlinks
        mkdir -p symlinks
        ln -s ../subdir/nested/file1.txt symlinks/link_to_file1.txt
        ln -s ../subdir/file2.txt symlinks/link_to_file2.txt
    >>>
    output {
        Array[File] matched_files_top = glob("subdir/*.txt")
        Array[File] matched_files_nested = glob("subdir/**/*.txt")
        Array[File] matched_symlinks = glob("symlinks/*.txt")
    }
}
