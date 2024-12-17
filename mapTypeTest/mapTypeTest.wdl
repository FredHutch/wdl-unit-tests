version 1.0
## This workflow demonstrates the usage of map types in WDL
## by processing sample read length data as an example.

#### WORKFLOW DEFINITION

workflow map_example {
    input {
        Array[String] samples = ["sample1", "sample2", "sample3"]
        Map[String, String] sample_metadata = {
            "sample1": "normal",
            "sample2": "tumor",
            "sample3": "normal"
        }
        Map[String, Int] read_lengths = {
            "sample1": 100,
            "sample2": 150,
            "sample3": 100
        }
    }

    # To iterate over a map in WDL 1.0, we need to provide the keys as an array, super annoying
    # WDL 1.1+ has a "keys" function that you can use to loop through the keys of the map
    scatter (sample in samples) {
        call process_sample {
            input:
                sample_name = sample,
                sample_type = sample_metadata[sample],
                read_length = read_lengths[sample]
        }
    }
}

#### TASK DEFINITIONS

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
        docker: "ubuntu:latest"
    }
}
