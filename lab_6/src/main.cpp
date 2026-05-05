#include <opencv2/opencv.hpp>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

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

    cv::createTrackbar("Brightness", display.getWindowName(), &FrameProcessor::brightnessValue, 100);
    cv::setMouseCallback(display.getWindowName(), onMouse, nullptr);

    cv::Mat frame;

    while (true) {
        if (!camera.getFrame(frame)) {
            break; 
        }

        frameProc.process(frame, keyProc.currentMode);
        display.show(frame);

        int key = cv::waitKey(30);
        if (key >= 0) {
            if (!keyProc.processKey(key)) {
                break; 
            }
        }
    }

    return 0;
}
