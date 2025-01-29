version 1.0
## This is a test workflow that returns the hostname of the node 
## the job is submitted to as a test for module functionality on Gizmo.
## Added verification of module loading.

#### WORKFLOW DEFINITION

workflow HelloModuleHostname {
  input {
    String module2load = "Python/3.12.3-GCCcore-13.3.0" # Default value can be overwritten
  }

  call Hostname {
    input:
      module_env = module2load
  }

  output {
    File stdout = Hostname.out
    Boolean module_loaded = Hostname.module_verified
  }

  parameter_meta {
    stdout: "hostname of the node the job was submitted to"
    module_loaded: "boolean indicating if the specified module was successfully loaded"
  }
}

#### TASK DEFINITIONS

task Hostname {
  input {
    String module_env
  }

  command <<<
    set -e  # Exit on any error
    
    # Get hostname
    hostname
    
    # List loaded modules and verify our module is loaded
    module list 2>&1 | tee module_list.txt
    
    # Extract just the module name without version for more flexible matching
    MODULE_BASE=$(echo "~{module_env}" | cut -d'/' -f1)
    
    # Check if the module or its base name is in the loaded modules
    if grep -q "~{module_env}\|${MODULE_BASE}/" module_list.txt; then
      echo "true" > module_verified.txt
      echo "Successfully verified module ~{module_env} is loaded"
    else
      echo "false" > module_verified.txt
      echo "ERROR: Module ~{module_env} was not found in loaded modules:"
      cat module_list.txt
      exit 1
    fi
  >>>

  output {
    File out = stdout()
    Boolean module_verified = read_boolean("module_verified.txt")
  }

  runtime {
    cpu: 1
    memory: "1 GB"
    modules: "~{module_env}"
  }

  parameter_meta {
    module_env: "name of modules to be loaded"
    out: "output file containing hostname and module information"
    module_verified: "boolean indicating if the requested module was successfully loaded"
  }
}
