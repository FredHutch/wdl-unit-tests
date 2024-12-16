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
    echo $(hostname)
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