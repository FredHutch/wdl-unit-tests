version 1.0

workflow jsonFileLocalization {
  input {
    # Required inputs
    File required_json_remote     # Remote JSON file
    
    # Optional inputs
    File? optional_json_remote
    File? optional_remote_not_provided
  }

  # Task to copy JSON files to the working directory
  call CopyJsons {
    input:
      required_remote = required_json_remote,
      optional_remote = optional_json_remote,
      optional_remote_not_provided = optional_remote_not_provided
  }

  output {
    Array[File] copied_files = CopyJsons.out_files
  }
}

task CopyJsons {
  input {
    File required_remote
    File? optional_remote
    File? optional_remote_not_provided
  }

  command <<<
    set -e
    mkdir -p copied_jsons
    
    # Copy the required local and remote files
    cp ~{required_remote} copied_jsons/$(basename ~{required_remote})
    cp ~{optional_remote} copied_jsons/$(basename ~{optional_remote})
    cp ~{optional_remote_not_provided} copied_jsons/$(basename ~{optional_remote_not_provided})
    
  >>>

  output {
    Array[File] out_files = glob("copied_jsons/*")
  }

  runtime {
    docker: "ubuntu:20.04"
  }
}
