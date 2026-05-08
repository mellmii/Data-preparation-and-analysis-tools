#include "FaceDetector.hpp"
#include <chrono>

FaceDetector::FaceDetector(const std::string& prototxt, const std::string& model) {
    net = cv::dnn::readNetFromCaffe(prototxt, model);
    running = true;
    hasNewFrame = false;
    workerThread = std::thread(&FaceDetector::detectLoop, this);
}

FaceDetector::~FaceDetector() {
    running = false;
    cv_frame.notify_one();
    if (workerThread.joinable()) {
        workerThread.join();
    }
}

void FaceDetector::setFrame(const cv::Mat& frame) {
    std::lock_guard<std::mutex> lock(mtx);
    frame.copyTo(currentFrame);
    hasNewFrame = true;
    cv_frame.notify_one();
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(mtx);
    return detectedFaces;
}

void FaceDetector::detectLoop() {
    while (running) {
        cv::Mat frameToProcess;
        {
            std::unique_lock<std::mutex> lock(mtx);
            cv_frame.wait(lock, [this] { return hasNewFrame || !running; });
            
            if (!running) break;
            
            currentFrame.copyTo(frameToProcess);
            hasNewFrame = false;
        }

        if (frameToProcess.empty()) continue;


        cv::Mat blob = cv::dnn::blobFromImage(frameToProcess, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
        net.setInput(blob);
        cv::Mat detections = net.forward();

        std::vector<cv::Rect> faces;
        cv::Mat detectionMat(detections.size[2], detections.size[3], CV_32F, detections.ptr<float>());

        for (int i = 0; i < detectionMat.rows; i++) {
            float confidence = detectionMat.at<float>(i, 2);
            if (confidence > 0.5) {
                int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frameToProcess.cols);
                int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frameToProcess.rows);
                int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frameToProcess.cols);
                int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frameToProcess.rows);
                faces.push_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
            }
        }

        {
            std::lock_guard<std::mutex> lock(mtx);
            detectedFaces = faces;
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
}
