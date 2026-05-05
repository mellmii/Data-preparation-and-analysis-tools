#pragma once

enum class ProcessingMode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY,
    GLITCH,
    HOLLOW_KNIGHT
};

class KeyProcessor {
public:
    ProcessingMode currentMode = ProcessingMode::NORMAL;
    bool processKey(int key);
};
