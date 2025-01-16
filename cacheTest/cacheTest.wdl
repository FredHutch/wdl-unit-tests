version 1.0

workflow CacheTest {
    input {
        String message
        Int sleep_time = 20
    }

    call GenerateTimestamp {
        input:
            input_message = message,
            sleep_seconds = sleep_time
    }

    output {
        File output_file = GenerateTimestamp.timestamp_file
    }
}

task GenerateTimestamp {
    input {
        String input_message
        Int sleep_seconds
    }

    command <<<
        sleep ~{sleep_seconds}
        
        # Use a deterministic identifier based on inputs
        echo "Message: ~{input_message}" > output.txt
        echo "Sleep time: ~{sleep_seconds}" >> output.txt
        echo "Run ID: ~{input_message}-~{sleep_seconds}" >> output.txt
    >>>

    output {
        File timestamp_file = "output.txt"
    }

    runtime {
        docker: "ubuntu:latest"
        cpu: 1
        memory: "1 GB"
    }
}
