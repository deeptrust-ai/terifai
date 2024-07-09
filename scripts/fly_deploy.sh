#!/bin/bash

# Source the set_wheel.sh script to get its exports
source ./scripts/set_wheel.sh

echo "WHEEL: $WHEEL"
echo "WHEEL_VERSION: $WHEEL_VERSION"

# Deploy with the WHEEL build argument
fly deploy --build-arg WHEEL=$WHEEL
