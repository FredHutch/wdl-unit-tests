version 1.0

workflow enhanced_map_test {
    input {
        # Original inputs
        Array[String] samples
        Map[String, String] sample_metadata
        Map[String, Int] read_lengths

        # New test inputs
        Map[String, Map[String, String]] nested_map = {
            "patient1": {
                "sample1": "normal",
                "sample2": "tumor"
            },
            "patient2": {
                "sample3": "normal",
                "sample4": "tumor"
            }
        }
        # We need to provide keys as arrays since WDL 1.0 doesn't have a keys() function
        Array[String] patient_ids = ["patient1", "patient2"]
    }

    # Test nested map processing
    scatter (patient_id in patient_ids) {
        call process_nested_map {
            input:
                patient_id = patient_id,
                patient_data = nested_map[patient_id],
                # We need to provide the sample names explicitly
                samples_for_patient = if patient_id == "patient1" then ["sample1", "sample2"] else ["sample3", "sample4"]
        }
    }

    # Original sample processing with output map generation
    scatter (sample in samples) {
        call process_sample {
            input:
                sample_name = sample,
                sample_type = sample_metadata[sample],
                read_length = read_lengths[sample]
        }
    }

    # Aggregate results into a map
    call create_result_map {
        input:
            sample_names = samples,
            processing_messages = process_sample.message
    }

    output {
        Map[String, String] result_map = create_result_map.output_map
        Array[String] nested_map_results = process_nested_map.message
    }
}

task process_nested_map {
    input {
        String patient_id
        Map[String, String] patient_data
        Array[String] samples_for_patient
    }

    # First get the first sample ID
    String first_sample = samples_for_patient[0]
    # Then use it to index the patient data
    String sample_type = patient_data[first_sample]

    command {
        echo "Processing patient ${patient_id} with sample type ${sample_type}"
        for sample in ${sep=' ' samples_for_patient}; do
            echo "Sample: $sample"
        done
    }

    output {
        String message = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:noble-20241118.1"
    }
}

task process_sample {
    input {
        String sample_name
        String sample_type
        Int read_length
    }

    command <<<
        echo "Processing ~{sample_name} (~{sample_type}) with read length ~{read_length}"
    >>>

    output {
        String message = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:noble-20241118.1"
    }
}

task create_result_map {
    input {
        Array[String] sample_names
        Array[String] processing_messages
    }

    command <<<
        python <<CODE
        samples = '~{sep="," sample_names}'.split(',')
        messages = '~{sep="," processing_messages}'.split(',')
        result = dict(zip(samples, messages))
        with open('output.txt', 'w') as f:
            for sample, message in result.items():
                f.write(f"{sample}\t{message}\n")
        CODE
    >>>

    output {
        Map[String, String] output_map = read_map('output.txt')
    }

    runtime {
        docker: "python:3.8-slim"
    }
}