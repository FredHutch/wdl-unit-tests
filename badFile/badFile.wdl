version 1.0
## This is a test workflow that fails against womtool.
## From https://github.com/broadinstitute/cromwell

#### WORKFLOW DEFINITION

workflow oops {
  call oopsie
}

#### TASK DEFINITIONS

task oopsie {
  input {
    String str
  }
  command { echo ${str} }
  runtime { docker: docker_image }
}
