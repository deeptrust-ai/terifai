#!/bin/bash

source ./scripts/set_wheel.sh

echo "WHEEL: $WHEEL"
echo "WHEEL_VERSION: $WHEEL_VERSION"

# Build the Docker image with the latest wheel
docker build --build-arg WHEEL=$WHEEL -t terifai:$WHEEL_VERSION -t terifai:latest .