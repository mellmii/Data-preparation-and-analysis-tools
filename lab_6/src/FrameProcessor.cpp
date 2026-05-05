#include "FrameProcessor.hpp"

int FrameProcessor::brightnessValue = 50; 
std::vector<cv::Point> FrameProcessor::drawnPoints;

void FrameProcessor::process(cv::Mat& frame, ProcessingMode mode) {
    frame.convertTo(frame, -1, 1, brightnessValue - 50);

    switch (mode) {
        case ProcessingMode::INVERT:
            cv::bitwise_not(frame, frame);
            break;
        case ProcessingMode::BLUR:
            cv::GaussianBlur(frame, frame, cv::Size(15, 15), 0);
            break;
        case ProcessingMode::CANNY:
            cv::cvtColor(frame, frame, cv::COLOR_BGR2GRAY);
            cv::Canny(frame, frame, 50, 150);
            cv::cvtColor(frame, frame, cv::COLOR_GRAY2BGR);
            break;
        case ProcessingMode::GLITCH: {
            std::vector<cv::Mat> channels;
            cv::split(frame, channels);
            cv::Mat shiftedR = cv::Mat::zeros(channels[2].size(), channels[2].type());
            int shift = 15;
            if (frame.cols > shift) {
                channels[2](cv::Rect(0, 0, frame.cols - shift, frame.rows))
                    .copyTo(shiftedR(cv::Rect(shift, 0, frame.cols - shift, frame.rows)));
            }
            channels[2] = shiftedR;
            cv::merge(channels, frame);
            break;
        }
        case ProcessingMode::HOLLOW_KNIGHT: {
            cv::Mat edges;
            cv::Canny(frame, edges, 60, 180);
            frame.setTo(cv::Scalar(0, 0, 0)); 
            frame.setTo(cv::Scalar(255, 200, 150), edges); 
            cv::GaussianBlur(frame, frame, cv::Size(3, 3), 0); 
            break;
        }
        default:
            break;
    }

    for (const auto& pt : drawnPoints) {
        int s = 12; 

        std::vector<std::vector<cv::Point>> triangle = {{
            cv::Point(pt.x, pt.y + s),
            cv::Point(pt.x - s, pt.y - s/4),
            cv::Point(pt.x + s, pt.y - s/4)
        }};
        
        cv::Scalar purple(200, 0, 150);


        cv::fillPoly(frame, triangle, purple);
        cv::circle(frame, cv::Point(pt.x - s/2, pt.y - s/4), s/2, purple, -1);
        cv::circle(frame, cv::Point(pt.x + s/2, pt.y - s/4), s/2, purple, -1);
    }


    cv::rectangle(frame, cv::Point(0, 0), cv::Point(frame.cols, 40), cv::Scalar(0, 0, 0), -1);

    cv::putText(frame, "Keys: 1-Norm 2-Inv 3-Blur 4-Canny 5-Glitch 6-Neon | R-Click: Clear", 
                cv::Point(10, 25), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255, 255, 255), 1);
}
