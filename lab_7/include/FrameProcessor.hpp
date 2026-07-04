#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    static int brightnessValue;
    static std::vector<cv::Point> drawnPoints;

    void process(cv::Mat& frame, ProcessingMode mode);
};
