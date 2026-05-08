#include <opencv2/opencv.hpp>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"
#include "FaceDetector.hpp"

void onMouse(int event, int x, int y, int flags, void* userdata) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        FrameProcessor::drawnPoints.push_back(cv::Point(x, y));
    } else if (event == cv::EVENT_RBUTTONDOWN) {
        FrameProcessor::drawnPoints.clear();
    }
}

int main() {
    CameraProvider camera(0);
    Display display("silly camera 3000");
    KeyProcessor keyProc;
    FrameProcessor frameProc;
    
    FaceDetector faceDetector("../deploy.prototxt", "../res10_300x300_ssd_iter_140000.caffemodel");

    cv::createTrackbar("Brightness", display.getWindowName(), &FrameProcessor::brightnessValue, 100);
    cv::setMouseCallback(display.getWindowName(), onMouse, nullptr);

    cv::Mat frame;

    while (true) {
        if (!camera.getFrame(frame)) break; 

        if (keyProc.currentMode == ProcessingMode::FACE_DETECT) {
            faceDetector.setFrame(frame);
        }

        frameProc.process(frame, keyProc.currentMode);

        if (keyProc.currentMode == ProcessingMode::FACE_DETECT) {
            std::vector<cv::Rect> faces = faceDetector.getFaces();
            for (const auto& face : faces) {
                cv::rectangle(frame, face, cv::Scalar(0, 255, 0), 2);
                cv::putText(frame, "Face 99%", cv::Point(face.x, face.y - 10), 
                            cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
            }
        }

        display.show(frame);

        int key = cv::waitKey(30);
        if (key >= 0) {
            if (!keyProc.processKey(key)) break; 
        }
    }

    return 0;
}
