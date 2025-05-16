#!/bin/bash

# Source the utility script with the find_tool function
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/find_tool.sh"

# Find the cromwell JAR
CROMWELL_PATH=$(find_cromwell)

# Check if cromwell was found
if [ -z "$CROMWELL_PATH" ]; then
    echo "Error: cromwell-87.jar not found on your system."
    echo "Please download it or specify the path manually by setting the CROMWELL_PATH environment variable."
    exit 1
fi

echo "Found cromwell at: $CROMWELL_PATH"
export CROMWELL_PATH

# Run tests on all WDL files
for i in $(find . -type f -name "*.wdl" -exec dirname {} \; | sort -u | sed 's|^\./||'); do
  echo "$i"
  uv run pytest tests/cromwelljava/test-run.py --wdl-path=$i --verbose -s
  echo -e "\n\n"
done
