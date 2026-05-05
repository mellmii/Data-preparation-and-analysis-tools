#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    static int brightnessValue; // Статичне поле для слайдера
    static std::vector<cv::Point> drawnPoints; // Точки для малювання мишкою

    void process(cv::Mat& frame, ProcessingMode mode);
};
