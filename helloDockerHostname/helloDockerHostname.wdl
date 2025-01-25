version 1.0
## This is a test workflow that returns the Docker image name and tag
## as a test for Docker functionality in WDL.

#### WORKFLOW DEFINITION

workflow HelloDockerHostname {
  input {
    String docker_image = "ubuntu:latest"  # Default value but can be overridden
  }

  call Hostname {
    input:
      expected_image = docker_image
  }

  output {
    File stdout = Hostname.out
  }

  parameter_meta {
    docker_image: "Docker image to run the task in (e.g. ubuntu:latest)"
  }
}

#### TASK DEFINITIONS

task Hostname {
  input {
    String expected_image
  }

  command <<<
    # Extract just the image name without tag for comparison
    EXPECTED_BASE_IMAGE=$(echo "~{expected_image}" | cut -d':' -f1)
    
    # Get Docker image info
    CURRENT_IMAGE=$(grep "ID=" /etc/os-release | head -n1 | cut -d'=' -f2)
    
    # Assert it's the expected image
    if [[ "$CURRENT_IMAGE" != "$EXPECTED_BASE_IMAGE" ]]; then
      echo "Error: Expected Docker image $EXPECTED_BASE_IMAGE but got: $CURRENT_IMAGE"
      exit 1
    fi
    
    # If assertion passes, print container info
    echo "Verified Docker Image: $CURRENT_IMAGE"
    echo "Expected Image: $EXPECTED_BASE_IMAGE"
    echo "Hostname: $(hostname)"
    echo "Container ID: $(grep -o -E '[[:alnum:]]{64}' /proc/1/cpuset || echo 'Not found')"
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
