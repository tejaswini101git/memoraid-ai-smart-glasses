# MEMORAID Software

> Reference software implementation for **MEMORAID — AI Smart Glasses for Dementia Assistance**

MEMORAID is an AI-assisted wearable concept designed to support people with dementia through camera-based face detection, contextual audio feedback, and caregiver notifications.

---

## ⚠️ Implementation Note

The original prototype software is not available as a complete historical codebase.

The software in this directory is a **reconstructed/reference implementation** based on the documented MEMORAID system architecture. It is intended for reproducible development, testing, and demonstration and should not be interpreted as the exact software used in the original physical prototype.

---

## System Architecture

```text
                    MEMORAID SOFTWARE PIPELINE

                         OV2640 Camera
                              │
                              ▼
                         ESP32-CAM
                              │
                              ▼
                      Image Acquisition
                              │
                              ▼
                       Face Detection
                          OpenCV
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Audio Feedback            Caregiver Alert
             pyttsx3                  Interface
                 │                         │
                 ▼                         ▼
           Audio Output              Notification
              Layer                     Layer
```

---

## Project Structure

```text
software/
├── audio/
│   └── audio_feedback.py
│
├── caregiver/
│   └── caregiver_alert.py
│
├── esp32_cam/
│   └── memoraid_camera.ino
│
├── face_recognition/
│   ├── recognizer.py
│   └── run_recognition.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Components

### 📷 ESP32-CAM

**File:** `esp32_cam/memoraid_camera.ino`

Reference firmware for the camera acquisition layer.

**Features:**

- AI Thinker ESP32-CAM configuration
- OV2640 camera initialization
- Wi-Fi connectivity
- JPEG image capture
- HTTP capture endpoint
- Device status endpoint

The ESP32-CAM represents the image acquisition layer of the MEMORAID system.

---

### 👤 Face Detection

**File:** `face_recognition/recognizer.py`

The current local reference implementation uses OpenCV's Haar Cascade detector.

**Capabilities:**

- Image loading
- Face detection
- Face bounding-box detection
- Reusable face-processing interface

> The current implementation performs **face detection only**. It does not claim to perform biometric identity recognition.

---

### 🔄 Recognition Pipeline

**File:** `face_recognition/run_recognition.py`

Connects the computer-vision module with the audio and caregiver layers.

The pipeline is designed to:

1. Load an input image
2. Detect a face
3. Generate a system response
4. Trigger the appropriate software output layer

---

### 🔊 Audio Feedback

**File:** `audio/audio_feedback.py`

Provides the software audio-feedback interface using `pyttsx3`.

**Supported events:**

- System startup
- Person detected
- Unknown person
- No person detected

For local testing, audio is generated through the computer's audio system.

In the physical prototype, this software layer corresponds to the audio amplifier and bone-conduction speaker output.

---

### 🚨 Caregiver Alert

**File:** `caregiver/caregiver_alert.py`

Provides a structured caregiver-notification interface.

The current implementation can:

- Create alert events
- Record timestamps
- Include an optional confidence value
- Print structured alerts for testing

The current implementation does **not** connect to a production messaging service.

---

## Requirements

The reference implementation was tested locally using:

- Python 3.12
- Windows
- OpenCV 4.13.0
- NumPy
- pyttsx3
- Flask
- Requests

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## Running the Face Detection Module

Navigate to:

```text
software/face_recognition
```

Then run:

```powershell
python recognizer.py
```

Expected output:

```text
MEMORAID face detection module initialized.
```

---

## Running the Recognition Pipeline

From the `face_recognition` directory:

```powershell
python run_recognition.py
```

The pipeline can also process an image directly:

```python
from run_recognition import MemoraidRecognitionPipeline

pipeline = MemoraidRecognitionPipeline()

result = pipeline.process_image(
    r"C:\path\to\image.jpg"
)

print(result)
```

---

## Local Verification

A sample image was processed using the OpenCV face detector.

### Face Detection Result

```text
Faces detected: 1
Boxes: [[43, 67, 88, 88]]
```

A separate output image was generated with a bounding box around the detected face.

### Pipeline Result

The reference pipeline produced:

```text
MEMORAID: Face detected is nearby.
```

This verifies the local image-processing path from:

```text
Input Image
     ↓
OpenCV Face Detection
     ↓
MEMORAID Pipeline
     ↓
System Response
```

---

## Caregiver Alert Verification

The caregiver alert interface was tested independently.

Example output:

```text
MEMORAID CAREGIVER ALERT
To: Caregiver
Event: Unknown person detected
Confidence: 87.0%
```

The resulting alert contains structured information including:

```text
Recipient
Event
Timestamp
Confidence
```

> The confidence value in this standalone interface test was manually supplied for interface testing. It is not a measured model confidence.

---

## Implementation Status

| Component | Status |
|---|---|
| ESP32-CAM reference firmware | ✅ Implemented |
| OV2640 camera initialization | ✅ Implemented |
| Local face detection | ✅ Implemented |
| Image-processing pipeline | ✅ Implemented |
| Audio feedback interface | ✅ Implemented |
| Caregiver alert interface | ✅ Implemented |
| Local software testing | ✅ Verified |
| Biometric identity recognition | 🔧 Future integration |
| Reference-face enrollment | 🔧 Future integration |
| Production caregiver notifications | 🔧 Future integration |
| Physical hardware integration testing | 🔧 Requires prototype hardware |
| Edge-device ML deployment | 🔧 Future integration |

---

## Future Development

- Integrate a dedicated face-recognition model
- Add reference-face enrollment
- Implement identity matching
- Evaluate recognition accuracy
- Measure false positives and false negatives
- Integrate physical audio hardware
- Connect a real caregiver notification service
- Add event logging
- Explore edge-device inference
- Optimize inference for embedded hardware

---

## Development Note

This software directory provides a reproducible reference implementation of the MEMORAID software architecture while maintaining a clear distinction between the reconstructed software and the original physical prototype.

The implementation can be extended as additional original design information, datasets, hardware interfaces, and deployment requirements become available.
