version 1.0
## This is a test workflow that returns the hostname of the node 
## the job is submitted to as a test for module functionality on Gizmo.

#### WORKFLOW DEFINITION

workflow HelloModuleHostname {
  call Hostname {
  }

  output {
    File stdout = Hostname.out
  }

  parameter_meta {
    stdout: "hostname of the node the job was submitted to"
  }
}

#### TASK DEFINITIONS

task Hostname {
  command <<<
    hostname
    # python_installation=$(which python)
    # if [[ $python_installation != "/app/software/Python/3.7.4-GCCcore-8.3.0/bin/python" ]]; then
    #     echo "ERROR: Wrong Python instance. Expected /app/software/Python/3.7.4-GCCcore-8.3.0/bin/python, got $python_installation" >&2
    #     exit 1
    # fi
    # echo "Using Python installation: $python_installation"
  >>>

  output {
    File out = stdout()
  }

  runtime {
    cpu: 1
    memory: "1 GB"
    modules: "Python/3.7.4-foss-2019b-fh1"
  }

  parameter_meta {
    out: "hostname of the node the job was submitted to"
  }
}
