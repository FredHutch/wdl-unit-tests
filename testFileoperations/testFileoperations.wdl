version 1.0

workflow testFileoperations {
    call file_operations

    output {
        File created_file1 = file_operations.created_file1
        File moved_file = file_operations.moved_file
        File renamed_file = file_operations.renamed_file
    }
}

task file_operations {
    command <<<
        # Create three different files
        echo "This is the first created file." > file1.txt
        echo "This is the second file that will be moved." > file2.txt
        echo "This is the third file that will be renamed." > file3.txt
        
        # Move the second file to a new directory
        mkdir -p output_dir
        mv file2.txt output_dir/
        
        # Rename the third file
        mv file3.txt file3_renamed.txt
    >>>

    output {
        # Output the actual existing files
        File created_file1 = "file1.txt"                  # The first file remains unchanged
        File moved_file = "output_dir/file2.txt"          # The second file after being moved
        File renamed_file = "file3_renamed.txt"           # The third file after being renamed
    }

    runtime {
        docker: "ubuntu:20.04"
    }
}
