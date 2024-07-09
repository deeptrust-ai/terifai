#!/bin/bash

# Find the latest wheel file
latest_wheel=$(ls -t dist/*.whl | head -1)

# Extract version from wheel filename, assuming the format NAME-VERSION-*.whl
# For example, deeptrust-api-0.1.0-py3-none-any.whl => 0.1.0
export WHEEL_VERSION=$(echo $latest_wheel | sed 's/[^-]*-\([^-]*\)-.*/\1/')
export WHEEL=$(basename $latest_wheel)