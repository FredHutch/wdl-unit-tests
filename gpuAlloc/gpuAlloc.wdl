version 1.0

# This workflow tests GPU allocation and basic tensor operations using TensorFlow
# It verifies that:
# 1. A GPU can be successfully allocated
# 2. TensorFlow can detect and use the GPU
# 3. Basic matrix multiplication works correctly

workflow GpuMatrixMult {
    call GpuTest

    output {
        File test_results = GpuTest.results
        Int gpu_count = GpuTest.detected_gpus
        Array[Float] matrix_result = GpuTest.multiplication_result
    }

    parameter_meta {
        test_results: "Complete log of the GPU test including tensor operations and GPU detection"
        gpu_count: "Number of GPUs detected by TensorFlow"
        matrix_result: "Results of the matrix multiplication operation"
    }
}

task GpuTest {
    command <<<
        python3 <<CODE
        import tensorflow as tf
        import numpy as np

        # Test GPU availability
        gpus = tf.config.experimental.list_physical_devices('GPU')
        print(f"Number of GPUs detected: {len(gpus)}")
        
        # Create test matrices
        matrix_a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3])
        matrix_b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2])
        
        # Perform matrix multiplication
        result = tf.matmul(matrix_a, matrix_b)
        
        # Print results
        print("\nMatrix A:")
        print(matrix_a.numpy())
        print("\nMatrix B:")
        print(matrix_b.numpy())
        print("\nMatrix Multiplication Result:")
        print(result.numpy())
        
        # Save results for output
        np.savetxt("multiplication_result.txt", result.numpy().flatten())
        with open("gpu_count.txt", "w") as f:
            f.write(str(len(gpus)))
        CODE
    >>>

    output {
        File results = stdout()
        Int detected_gpus = read_int("gpu_count.txt")
        Array[Float] multiplication_result = read_lines("multiplication_result.txt")
    }

    runtime {
        docker: "tensorflow/tensorflow:latest-gpu"
        gpus: "1"
    }

    parameter_meta {
        results: "Output log containing GPU detection and matrix multiplication results"
        detected_gpus: "Number of GPUs detected by TensorFlow"
        multiplication_result: "Flattened array containing the result of matrix multiplication"
    }
}
