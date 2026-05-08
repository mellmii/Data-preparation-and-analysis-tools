#include "KeyProcessor.hpp"

bool KeyProcessor::processKey(int key) {
    if (key == 27) return false;
    
    if (key == 'f' || key == 'F') {
        currentMode = ProcessingMode::FACE_DETECT;
        return true;
    }
    
    switch (key) {
        case '1': currentMode = ProcessingMode::NORMAL; break;
        case '2': currentMode = ProcessingMode::INVERT; break;
        case '3': currentMode = ProcessingMode::BLUR; break;
        case '4': currentMode = ProcessingMode::CANNY; break;
        case '5': currentMode = ProcessingMode::GLITCH; break;
        case '6': currentMode = ProcessingMode::HOLLOW_KNIGHT; break;
    }
    
    return true;
}
