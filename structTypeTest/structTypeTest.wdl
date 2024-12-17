version 1.0
## This workflow demonstrates the usage of struct types in WDL
## by organizing sample metadata in a structured format

#### STRUCT DEFINITIONS

struct SampleInfo {
    String name
    String type
    Int read_length
    Float quality_score
}

#### WORKFLOW DEFINITION

workflow struct_example {
    input {
        Array[SampleInfo] sample_information
    }

    scatter (sample_info in sample_information) {
        call process_sample {
            input:
                sample = sample_info
        }
    }
}

#### TASK DEFINITIONS

task process_sample {
    input {
        SampleInfo sample
    }

    command <<<
        echo "Processing ~{sample.name} (~{sample.type})"
        echo "Read Length: ~{sample.read_length}"
        echo "Quality Score: ~{sample.quality_score}"
    >>>

    output {
        String message = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:latest"
    }
}
