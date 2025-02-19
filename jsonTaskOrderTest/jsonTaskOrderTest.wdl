version 1.0

workflow jsonTaskOrderTest {
  input {
    String input_json  # JSON string used as input for both tasks
  }

  call Task1 { input: input_json = input_json }
  call Task2 { input: input_json = input_json, previous_output = Task1.output_file }

  output {
    File task1_output = Task1.output_file
    File task2_output = Task2.output_file
  }
}

task Task1 {
  input {
    String input_json
  }
  
  command <<<
    echo "Processing JSON in Task1: ~{input_json}" > task1_output.txt
    echo "Task1 completed" >> task1_output.txt
  >>>
  
  output {
    File output_file = "task1_output.txt"
  }
  
  runtime {
    cpu: 1
    memory: "2G"
  }
}

task Task2 {
  input {
    String input_json
    File previous_output
  }
  
  command <<<
    echo "Processing JSON in Task2: ~{input_json}" > task2_output.txt
    echo "Task2 completed after Task1" >> task2_output.txt
    cat ~{previous_output} >> task2_output.txt
  >>>
  
  output {
    File output_file = "task2_output.txt"
  }
  
  runtime {
    cpu: 1
    memory: "2G"
  }
}
