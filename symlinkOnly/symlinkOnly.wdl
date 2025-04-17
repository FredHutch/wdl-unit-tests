version 1.0

workflow symlinkOnly {
    call generate_diverse_outputs
    
    output {
        File symlink_file = generate_diverse_outputs.symlink_output
    }
}

task generate_diverse_outputs {
    command <<<
        # Create a symlink
        echo "original" > original.txt
        ln -s original.txt link.txt
    >>>

    output {
        File symlink_output = "link.txt"
    }

    runtime {
        docker: "ubuntu:noble-20241118.1"
    }
}
