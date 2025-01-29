version 1.0

workflow jsonFileLocalization {
  input {
    # Required inputs
    File required_json_local      # Local JSON file
    File required_json_remote     # Remote JSON file
    
    # Optional inputs
    File? optional_json_local
    File? optional_json_remote
    File? optional_remote_not_provided
  }

  # Task to copy JSON files to the working directory
  call CopyJsons {
    input:
      required_local = required_json_local,
      required_remote = required_json_remote,
      optional_local = optional_json_local,
      optional_remote = optional_json_remote,
      optional_remote_not_provided = optional_remote_not_provided
  }

  output {
    Array[File] copied_files = CopyJsons.out_files
  }
}

task CopyJsons {
  input {
    File required_local
    File required_remote
    File? optional_local
    File? optional_remote
    File? optional_remote_not_provided
  }

  command <<<
    set -e
    mkdir -p copied_jsons
    
    # Copy the required local and remote files
    cp ~{required_local} copied_jsons/$(basename ~{required_local})
    cp ~{required_remote} copied_jsons/$(basename ~{required_remote})
    
    # Copy optional files if they exist
    if [[ -n "~{optional_local}" && -f "~{optional_local}" ]]; then
      cp ~{optional_local} copied_jsons/$(basename ~{optional_local})
    fi

    if [[ -n "~{optional_remote}" && -f "~{optional_remote}" ]]; then
      cp ~{optional_remote} copied_jsons/$(basename ~{optional_remote})
    fi

    if [[ -n "~{optional_remote_not_provided}" && -f "~{optional_remote_not_provided}" ]]; then
      cp ~{optional_remote_not_provided} copied_jsons/$(basename ~{optional_remote_not_provided})
    fi
    
  >>>

  output {
    Array[File] out_files = glob("copied_jsons/*")
  }

  runtime {
    docker: "ubuntu:20.04"
  }
}
