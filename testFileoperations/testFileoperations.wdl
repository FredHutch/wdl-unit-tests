version 1.0

workflow testFileoperations {
    call file_operations

    output {
        File created_file = file_operations.created_file
        File moved_file = file_operations.moved_file
        File renamed_file = file_operations.renamed_file
    }
}

task file_operations {
    command <<<
        # Create a new file
        echo "This is the created file." > created_file.txt
        
        # Move the created file to a new directory
        mkdir -p output_dir
        mv created_file.txt output_dir/
        
        # Rename the moved file
        mv output_dir/created_file.txt output_dir/renamed_file.txt
    >>>

    output {
        File created_file = "created_file.txt"  # This will fail if not created correctly
        File moved_file = "output_dir/created_file.txt"  # Verifies file was moved
        File renamed_file = "output_dir/renamed_file.txt"  # Verifies file was renamed
    }

    runtime {
        docker: "ubuntu:20.04"
    }
}
