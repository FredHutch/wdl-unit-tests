version 1.0
## This workflow demonstrates the usage of struct and map types in WDL
## by processing user information and configuration settings.

#### TYPE DEFINITIONS

struct User {
    String name
    Int age
    Map[String, String] preferences
}

#### WORKFLOW DEFINITION

workflow StructAndMapTypes {
    input {
        User user
        Map[String, Int] scores
    }
    
    call ProcessUser { 
        input: 
            person = user,
            test_scores = scores
    }
    
    output {
        String user_summary = ProcessUser.summary
        Map[String, Int] processed_scores = ProcessUser.updated_scores
    }

    parameter_meta {
        user: "User struct containing name, age, and preferences"
        scores: "Map of test names to scores"
    }
}

#### TASK DEFINITIONS

task ProcessUser {
    input {
        User person
        Map[String, Int] test_scores
    }
    
    command <<<
        echo "User Summary:" > summary.txt
        echo "Name: ~{person.name}" >> summary.txt
        echo "Age: ~{person.age}" >> summary.txt
        echo "Preferences:" >> summary.txt
        ~{write_map(person.preferences)} >> summary.txt
        echo "Test Scores:" >> summary.txt
        ~{write_map(test_scores)} >> summary.txt
    >>>
    
    output {
        String summary = read_string("summary.txt")
        Map[String, Int] updated_scores = test_scores
    }
    
    runtime {
        cpu: 1
        memory: "1 GB"
    }

    parameter_meta {
        person: "User struct to process"
        test_scores: "Map of test scores to process"
    }
}
