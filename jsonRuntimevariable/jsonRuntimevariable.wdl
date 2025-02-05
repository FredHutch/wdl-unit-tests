version 1.0

workflow jsonRuntimevariable {
  call CpuTest
  call MemoryTest
  call RetryTest
  #call ContinueTest
  call StderrTest

  output {
    File cpuTestOutput = CpuTest.metadataFile
    File memoryTestOutput = MemoryTest.metadataFile
    File retryTestOutput = RetryTest.metadataFile
    #File continueTestOutput = ContinueTest.metadataFile
    File stderrTestOutput = StderrTest.metadataFile
  }
}

task CpuTest {
  input {
    Int cpu = 1  # Default value; can be overridden in runtime
  }
  command <<<
    # Write runtime attributes to a metadata file
    echo "CPU: ~{cpu}" > metadata.txt
    echo "Task: CpuTest" >> metadata.txt
    echo "Status: Success" >> metadata.txt
  >>>
  output {
    File metadataFile = "metadata.txt"
  }
  runtime {
    cpu: cpu  # Use the input value
  }
}

task MemoryTest {
  input {
    String memory = "2G"  # Default value; can be overridden in runtime
  }
  command <<<
    # Write runtime attributes to a metadata file
    echo "Memory: ~{memory}" > metadata.txt
    echo "Task: MemoryTest" >> metadata.txt
    echo "Status: Success" >> metadata.txt
  >>>
  output {
    File metadataFile = "metadata.txt"
  }
  runtime {
    memory: memory  # Use the input value
  }
}

task RetryTest {
  input {
    Int maxRetries = 2
  }
  command <<<
    # Simulate a transient failure without tracking retries via files
    # Cromwell retries automatically up to `maxRetries`
    # This script fails 50% of the time for demonstration
    if [ $(( RANDOM % 2 )) -eq 0 ]; then
      echo "Attempt succeeded immediately." > metadata.txt
      echo "MaxRetries: ~{maxRetries}" >> metadata.txt
      echo "Task: RetryTest" >> metadata.txt
      echo "Status: Success" >> metadata.txt
      exit 0
    else
      echo "Simulating transient failure..." >&2
      exit 1
    fi
  >>>
  output {
    File metadataFile = "metadata.txt"
  }
  runtime {
    maxRetries: maxRetries
    failOnStderr: false  # Ensure stderr does not fail the task
  }
}

task ContinueTest {
  input {
    Array[Int] continueOnReturnCode
  }
  command <<<
    echo "ContinueOnReturnCode: ~{sep=',' continueOnReturnCode}" > metadata.txt
    echo "Task: ContinueTest" >> metadata.txt
    echo "Status: Success (exit code 1 allowed)" >> metadata.txt
    exit 1  # Ensure this exits with code 1
  >>>
  output {
    File metadataFile = "metadata.txt"
  }
  runtime {
    continueOnReturnCode: continueOnReturnCode
    failOnStderr: false  # Add this to override the global setting
  }
}

task StderrTest {
  input {
    Boolean failOnStderr = false  # Default value; can be overridden in runtime
  }
  command <<<
    # Simulate stderr output but allow the task to succeed
    echo "FailOnStderr: ~{failOnStderr}" > metadata.txt
    echo "Task: StderrTest" >> metadata.txt
    echo "Status: Success (stderr output ignored)" >> metadata.txt
    echo "Error message (simulated)" >&2
  >>>
  output {
    File metadataFile = "metadata.txt"
  }
  runtime {
    failOnStderr: failOnStderr  # Use the input value
  }
}
