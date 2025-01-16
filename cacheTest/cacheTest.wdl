version 1.0

workflow CacheTest {
    input {
        String message
        Int sleep_time = 5
    }

    call GenerateTimestamp {
        input:
            input_message = message,
            sleep_seconds = sleep_time
    }

    output {
        File output_file = GenerateTimestamp.timestamp_file
        String execution_id = GenerateTimestamp.execution_id
    }
}

task GenerateTimestamp {
    input {
        String input_message
        Int sleep_seconds
    }

    command <<<
        # Sleep to make the task take a noticeable amount of time
        sleep ~{sleep_seconds}

        # Generate a unique execution ID
        execution_id=$(date +%s%N)
        echo "Execution ID: $execution_id"

        # Create output with timestamp and message
        echo "Message: ~{input_message}" > output.txt
        echo "Timestamp: $(date)" >> output.txt
        echo "Execution ID: $execution_id" >> output.txt
    >>>

    output {
        File timestamp_file = "output.txt"
        String execution_id = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:latest"
        cpu: 1
        memory: "1 GB"
    }
}
