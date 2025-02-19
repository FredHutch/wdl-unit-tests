version 1.0

# The basicTaskTest workflow calls a task named simpleTask, which takes a string input and writes it to a file called output.txt. It demonstrates a basic execution of a task with file output.

# This tests basic task execution, input handling, and file output functionality. It ensures that a task can successfully take an input and generate an output.

workflow basicTaskTest {
  input {
    String text = "Hello, World!"
  }

  call simpleTask {
    input:
      message = text
  }
}

task simpleTask {
  input {
    String message
  }

  command <<<
    echo "~{message}" > output.txt
  >>>

  output {
    File outputFile = "output.txt"
  }

  runtime {
    docker: "ubuntu:20.04"
  }
}
