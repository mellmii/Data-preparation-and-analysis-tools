#!/bin/bash
echo "Installing dependencies..."
sudo apt update
sudo apt install -y build-essential cmake libopencv-dev wget

echo "Downloading DNN models for Face Detection..."
wget -nc -q -O deploy.prototxt https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
wget -nc -q -O res10_300x300_ssd_iter_140000.caffemodel https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel

echo "Dependencies and models installed successfully!"
