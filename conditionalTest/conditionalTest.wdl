version 1.0
## This workflow demonstrates the usage of conditional statements in WDL
## by selectively processing samples based on their properties

struct SampleInfo {
    String name
    Float quality_score
    String type
}

workflow conditional_example {
    input {
        Array[SampleInfo] samples
        Float quality_threshold
    }

    # Demonstrate if statement in scatter
    scatter (sample in samples) {
        if (sample.quality_score >= quality_threshold) {
            call process_high_quality {
                input:
                    sample = sample
            }
        }
    }

    # Create string arrays for the QC report
    scatter (sample in samples) {
        String sample_line = "~{sample.name},~{sample.type},~{sample.quality_score}"
    }

    # Demonstrate single conditional task
    call run_qc_report {
        input:
            sample_lines = sample_line
    }

    # Calculate number of high quality samples
    Int num_high_quality = length(select_all(process_high_quality.message))

    # Demonstrate separate conditional blocks (WDL 1.0 approach instead of if/else)
    Boolean has_multiple_samples = num_high_quality > 1
    
    if (has_multiple_samples) {
        call summarize {
            input:
                messages = select_all(process_high_quality.message),
                report = "Multiple high-quality samples processed"
        }
    }

    if (!has_multiple_samples) {
        call summarize as summarize_few {
            input:
                messages = select_all(process_high_quality.message),
                report = "Few or no high-quality samples found"
        }
    }

    output {
        String final_summary = select_first([summarize.summary, summarize_few.summary])
        File qc_report = run_qc_report.report_csv
    }
}

task process_high_quality {
    input {
        SampleInfo sample
    }

    command <<<
        echo "Processing high quality ~{sample.type} sample ~{sample.name} (Q=~{sample.quality_score})"
    >>>

    output {
        String message = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:noble-20241118.1"
    }
}

task run_qc_report {
    input {
        Array[String] sample_lines
    }

    command <<<
        echo "Quality Score Summary:"
        echo "Sample Name,Type,Quality Score" > report.csv
        ~{sep="\n" sample_lines} >> report.csv
        cat report.csv
    >>>

    output {
        String report = read_string(stdout())
        File report_csv = "report.csv"
    }

    runtime {
        docker: "ubuntu:noble-20241118.1"
    }
}

task summarize {
    input {
        Array[String] messages
        String report
    }

    command <<<
        echo "~{report}"
        echo "Number of samples processed: ~{length(messages)}"
    >>>

    output {
        String summary = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:noble-20241118.1"
    }
}
