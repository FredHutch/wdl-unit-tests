version 1.0
## This is a test workflow that returns the Docker image name and tag
## as a test for Docker functionality in WDL.

#### WORKFLOW DEFINITION

workflow HelloDockerHostname {
  input {
    String docker_image = "ubuntu:20.04"  # Default value but can be overridden
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
