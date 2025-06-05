#!/bin/bash

# Find a Cromwell-related JAR file
find_jar() {
    local jar_name="$1"
    local env_var_name="$2"

    # Check if environment variable is already set
    if [ ! -z "${!env_var_name}" ]; then
        # Verify the path exists
        if [ -f "${!env_var_name}" ]; then
            echo "${!env_var_name}"
            return 0
        else
            echo "Warning: $env_var_name is set but file does not exist: ${!env_var_name}" >&2
        fi
    fi

    # Check common locations for the JAR file
    possible_locations=(
        # Home directory and subdirectories
        "$HOME/*/$jar_name"
        "$HOME/*/*/$jar_name"
        "$HOME/*/*/*/$jar_name"
        "$HOME/*/*/*/*/$jar_name"
        # Current directory and subdirectories
        "./*/$jar_name"
        "./*/*/$jar_name"
        "./*/*/*/$jar_name"
        # Common specific paths
        "$HOME/github/cromwell/$jar_name"
        "$HOME/cromwell/$jar_name"
        "$HOME/Downloads/$jar_name"
    )

    # Look through each location
    for pattern in "${possible_locations[@]}"; do
        found_paths=$(find ${pattern} 2>/dev/null)
        if [ ! -z "$found_paths" ]; then
            # Take the first match
            echo "$found_paths" | head -n 1
            return 0
        fi
    done

    # If not found in common locations, do a broader search
    echo "$jar_name not found in common locations. Performing a broader search (this may take a while)..." >&2

    # Search in home directory (limit depth to avoid excessive searching)
    found_path=$(find "$HOME" -name "$jar_name" -type f -depth -10 2>/dev/null | head -n 1)

    if [ ! -z "$found_path" ]; then
        echo "$found_path"
        return 0
    fi

    # Not found
    echo ""
    return 1
}

# Wrapper function for womtool-87.jar
find_womtool() {
    find_jar "womtool-87.jar" "WOMTOOL_PATH"
}

# Wrapper function for cromwell-87.jar
find_cromwell() {
    find_jar "cromwell-87.jar" "CROMWELL_PATH"
}

# If this script is being executed directly, run the functions
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Finding womtool:"
    find_womtool
    echo "Finding cromwell:"
    find_cromwell
fi
