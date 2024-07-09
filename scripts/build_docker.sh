#!/bin/bash

# Find the latest wheel file
latest_wheel=$(ls -t dist/*.whl | head -1)

# Extract version from wheel filename, assuming the format NAME-VERSION-*.whl
# For example, deeptrust-api-0.1.0-py3-none-any.whl => 0.1.0
wheel_version=$(echo $latest_wheel | sed 's/[^-]*-\([^-]*\)-.*/\1/')
wheel=$(basename $latest_wheel)
# Build the Docker image with the latest wheel
docker build --build-arg wheel=$(basename $latest_wheel) -t terifai:$wheel_version -t terifai:latest .