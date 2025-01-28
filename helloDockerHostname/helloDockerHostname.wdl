version 1.0
## This is a test workflow that returns the Docker image name and tag
## and measures execution time of the Hostname task.

#### WORKFLOW DEFINITION

workflow HelloDockerHostname {
  input {
    String docker_image = "ubuntu:20.04"  # Default value but can be overridden
  }

  call GetStartTime

  call Hostname {
    input:
      expected_image = docker_image,
      start_time = GetStartTime.timestamp  # Add dependency on start time
  }

  call GetEndTime {
    input:
      hostname_done = Hostname.out  # Add dependency on Hostname completion
  }

  call ValidateExecutionTime {
    input:
      start_time = GetStartTime.timestamp,
      end_time = GetEndTime.timestamp
  }

  output {
    File stdout = Hostname.out
    Float execution_time_seconds = ValidateExecutionTime.duration_seconds
    Boolean within_time_limit = ValidateExecutionTime.within_limit
  }

  parameter_meta {
    docker_image: "Docker image to run the task in (e.g. ubuntu:latest)"
  }
}

#### TASK DEFINITIONS

task GetStartTime {
  command <<<
    date +%s.%N
  >>>

  output {
    Float timestamp = read_float(stdout())
  }

  runtime {
    docker: "ubuntu:20.04"
    cpu: 1
    memory: "1 GB"
  }
}

task GetEndTime {
  input {
    File hostname_done  # Add dependency on Hostname completion
  }

  command <<<
    date +%s.%N
  >>>

  output {
    Float timestamp = read_float(stdout())
  }

  runtime {
    docker: "ubuntu:20.04"
    cpu: 1
    memory: "1 GB"
  }
}

task ValidateExecutionTime {
  input {
    Float start_time
    Float end_time
  }

  command <<<
    # Calculate duration using awk for floating point arithmetic
    duration=$(awk "BEGIN {print ~{end_time} - ~{start_time}}")
    echo "$duration" > duration.txt
    
    # Check if duration is less than 120 seconds (2 minutes)
    awk -v dur="$duration" 'BEGIN {if (dur < 120) exit 0; exit 1}'
    if [ $? -eq 0 ]; then
      echo "true" > within_limit.txt
    else
      echo "false" > within_limit.txt
    fi
  >>>

  output {
    Float duration_seconds = read_float("duration.txt")
    Boolean within_limit = read_boolean("within_limit.txt")
  }

  runtime {
    docker: "ubuntu:20.04"
    cpu: 1
    memory: "1 GB"
  }
}

task Hostname {
  input {
    String expected_image
    Float start_time  # Add start_time as input to create dependency
  }

  command <<<
    # Split expected image into name and tag
    EXPECTED_IMAGE_NAME=$(echo "~{expected_image}" | cut -d':' -f1)
    EXPECTED_TAG=$(echo "~{expected_image}" | cut -d':' -f2)

    # Get current image info
    CURRENT_IMAGE=$(grep "ID=" /etc/os-release | head -n1 | cut -d'=' -f2)
    CURRENT_VERSION=$(grep "VERSION_ID=" /etc/os-release | cut -d'"' -f2)

    # Compare image name
    if [[ "$CURRENT_IMAGE" != "$EXPECTED_IMAGE_NAME" ]]; then
      echo "Error: Expected Docker image $EXPECTED_IMAGE_NAME but got: $CURRENT_IMAGE"
      exit 1
    fi

    # Compare version/tag
    if [[ "$CURRENT_VERSION" != "$EXPECTED_TAG" ]]; then
      echo "Error: Expected version $EXPECTED_TAG but got: $CURRENT_VERSION"
      exit 1
    fi

    echo "Verified Docker Image: $CURRENT_IMAGE:$CURRENT_VERSION"
    echo "Expected Image: ~{expected_image}"
    echo "Hostname: $(hostname)"
  >>>

  output {
    File out = stdout()
  }

  runtime {
    cpu: 1
    memory: "1 GB"
    docker: "~{expected_image}"
  }

  parameter_meta {
    expected_image: "Docker image that should be running this task"
  }
}
