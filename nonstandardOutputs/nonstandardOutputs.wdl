version 1.0

workflow test_nonstandard_outputs {
    call generate_diverse_outputs
    
    output {
        File special_chars = generate_diverse_outputs.file_special_chars
        File no_extension = generate_diverse_outputs.file_no_extension
        File nested_output = generate_diverse_outputs.nested_file
        File symlink_file = generate_diverse_outputs.symlink_output
        Array[File] glob_files = generate_diverse_outputs.pattern_files
    }
}

task generate_diverse_outputs {
    command <<<
        # File with special characters
        echo "test content" > "test@file#1.txt"
        
        # File without extension
        echo "no extension" > datafile
        
        # Nested directory output
        mkdir -p nested/dir
        echo "nested content" > nested/dir/test.txt
        
        # Create a symlink
        echo "original" > original.txt
        ln -s original.txt link.txt
        
        # Multiple pattern files
        for i in {1..3}; do
            echo "pattern $i" > "pattern_$i.out"
        done
    >>>

    output {
        File file_special_chars = "test@file#1.txt"
        File file_no_extension = "datafile"
        File nested_file = "nested/dir/test.txt"
        File symlink_output = "link.txt"
        Array[File] pattern_files = glob("pattern_*.out")
    }

    runtime {
        docker: "ubuntu:noble-20241118.1@sha256:80dd3c3b9c6cecb9f1667e9290b3bc61b78c2678c02cbdae5f0fea92cc6734ab"
    }
}
