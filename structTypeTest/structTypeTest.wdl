version 1.0

## This workflow demonstrates advanced struct features in WDL including:
## 1. Optional fields
## 2. Nested structs
## 3. Default values (handled in the workflow)

#### STRUCT DEFINITIONS

# Nested struct for sequencing metadata
struct SequencingInfo {
    String platform
    String? flowcell_id
    Int? lane_number
}

# Nested struct for quality metrics
struct QualityMetrics {
    Float quality_score
    Float? gc_content
    Int? duplicate_rate
}

# Main struct with nested structures and optional fields
struct SampleInfo {
    String name
    String? type
    Int? read_length
    String? library_prep
    SequencingInfo sequencing
    QualityMetrics metrics
}

#### WORKFLOW DEFINITION

workflow struct_example {
    input {
        Array[SampleInfo] sample_information
    }

    scatter (sample_info in sample_information) {
        SampleInfo processed_sample = object {
            name: sample_info.name,
            type: select_first([sample_info.type, "normal"]),
            read_length: select_first([sample_info.read_length, 100]),
            library_prep: sample_info.library_prep,
            sequencing: sample_info.sequencing,
            metrics: sample_info.metrics
        }

        call process_sample {
            input:
                sample = processed_sample
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
        echo "Sequencing Platform: ~{sample.sequencing.platform}"
        echo "Flowcell ID: ~{select_first([sample.sequencing.flowcell_id, 'N/A'])}"
        echo "Lane Number: ~{select_first([sample.sequencing.lane_number, -1])}"
        echo "Quality Score: ~{sample.metrics.quality_score}"
        echo "GC Content: ~{select_first([sample.metrics.gc_content, 0])}"
        echo "Duplicate Rate: ~{select_first([sample.metrics.duplicate_rate, 0])}%"
        echo "Library Prep: ~{select_first([sample.library_prep, 'Standard'])}"
    >>>

    output {
        String message = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:noble-20241118.1"
    }
}
