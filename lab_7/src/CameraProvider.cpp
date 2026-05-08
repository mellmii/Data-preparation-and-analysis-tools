#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider(int deviceId) {
    cap.open(deviceId);
    if (!cap.isOpened()) {
        std::cerr << "Error: Cannot open camera!" << std::endl;
    }
}

CameraProvider::~CameraProvider() {
    cap.release();
}

bool CameraProvider::getFrame(cv::Mat& frame) {
    cap >> frame;
    return !frame.empty();
}
