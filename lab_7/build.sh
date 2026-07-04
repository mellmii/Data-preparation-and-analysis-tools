#!/bin/bash
echo "Building the project..."
mkdir -p build
cd build
cmake ..
make
echo "Build complete!"
