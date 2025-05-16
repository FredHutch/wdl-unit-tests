#!/bin/bash

# Source the utility script with the find_tool function
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/find_tool.sh"

# Find the womtool JAR
WOMTOOL_PATH=$(find_tool)

# Check if womtool was found
if [ -z "$WOMTOOL_PATH" ]; then
    echo "Error: womtool-87.jar not found on your system."
    echo "Please download it or specify the path manually by setting the WOMTOOL_PATH environment variable."
    exit 1
fi

echo "Found womtool at: $WOMTOOL_PATH"
export WOMTOOL_PATH

# Run tests on all WDL files
for i in $(find . -type f -name "*.wdl" -exec dirname {} \; | sort -u | sed 's|^\./||'); do
  echo "$i"
  uv run pytest tests/cromwelljava/test-validate.py --wdl-path=$i --verbose -s
  echo -e "\n\n"
done
