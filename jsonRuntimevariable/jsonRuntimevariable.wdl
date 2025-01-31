version 1.0

workflow jsonRuntimevariable {
  call CpuTest
  call MemoryTest
  call RetryTest
  call ContinueTest
  call StderrTest

  output {
    File cpuTestOutput = CpuTest.metadataFile
    File memoryTestOutput = MemoryTest.metadataFile
    File retryTestOutput = RetryTest.metadataFile
    File continueTestOutput = ContinueTest.metadataFile
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
    Int maxRetries = 2  # Default value; can be overridden in runtime
  }
  command <<<
    # Simulate a transient failure but ensure the task eventually succeeds
    if [ -e retry_count.txt ]; then
      retries=$(cat retry_count.txt)
    else
      retries=0
    fi

    if [ $retries -lt ~{maxRetries} ]; then
      echo "Attempt failed (simulated). Retry count: $retries" >&2
      echo $((retries + 1)) > retry_count.txt
      exit 1
    else
      echo "Attempt succeeded after retries." >&2
      echo "MaxRetries: ~{maxRetries}" > metadata.txt
      echo "Task: RetryTest" >> metadata.txt
      echo "Status: Success after retries" >> metadata.txt
      exit 0
    fi
  >>>
  output {
    File metadataFile = "metadata.txt"
  }
  runtime {
    maxRetries: maxRetries  # Use the input value
  }
}

task ContinueTest {
  input {
    Array[Int] continueOnReturnCode = [1]  # Default value; can be overridden in runtime
  }
  command <<<
    # Simulate a non-zero exit code but allow the task to succeed
    echo "ContinueOnReturnCode: ~{continueOnReturnCode}" > metadata.txt
    echo "Task: ContinueTest" >> metadata.txt
    echo "Status: Success (exit code 1 allowed)" >> metadata.txt
    exit 1
  >>>
  output {
    File metadataFile = "metadata.txt"
  }
  runtime {
    continueOnReturnCode: continueOnReturnCode  # Use the input value
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
