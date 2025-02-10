version 1.0

# Define the structure for sampleDetails
struct sampleDetails {
    String experimentType
    String prepMethod
    String tissueType
}

# Define the main structure for the single sample
struct singleSample {
    String sampleName
    String aboutSample
    String sampleDescription
    sampleDetails details  # Use the sampleDetails struct here
}

workflow testNestedJsonArray {
  input {
    String cellNumber
    Array[singleSample] batchOfSamples  # Array of objects representing each sample
  }

  scatter (sample in batchOfSamples) {
    call processSample {
      input:
        sample = sample,
        base_file_name = sample.sampleName 
    }
  }

  output {
    # Collect all the fields together from each sample into one list
    Array[File] result_allSampleInfo = processSample.allSampleInfo
  }
}

task processSample {
  input {
    singleSample sample  # Use singleSample type, not Object
    String base_file_name
  }

  command <<<
    # Format the sample information as a single string
    allSampleInfo="~{sample.sampleName} | ~{sample.aboutSample} | ~{sample.sampleDescription} | ~{sample.details.experimentType} | ~{sample.details.prepMethod} | ~{sample.details.tissueType}"
    
    # Output the concatenated sample info to a file
    echo ${allSampleInfo} > ~{base_file_name}.allSampleInfo.txt
  >>>

  output {
    # Read all sample info from the file and output it as an Array of Strings
    File allSampleInfo = "${base_file_name}.allSampleInfo.txt"
  }

  runtime {
    docker: "ubuntu:20.04"
  }
}
