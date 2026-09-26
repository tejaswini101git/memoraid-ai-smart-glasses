# MEMORAID Software

This directory contains the software reference implementation for **MEMORAID**, an AI-assisted smart wearable concept designed to support people with dementia through face detection, contextual audio feedback, and caregiver notifications.

> **Implementation note**
>
> The original prototype software is not available as a complete historical codebase. The Python and ESP32-CAM modules in this directory are therefore a **reconstructed/reference implementation** created to demonstrate the intended software architecture and provide a reproducible development baseline.
>
> They should not be interpreted as the exact software that was used in the original physical prototype.

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │     OV2640 Camera   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    ESP32-CAM        │
                    │  Image Acquisition  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Face Detection     │
                    │  OpenCV Reference   │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌─────────────────┐   ┌──────────────────┐
          │ Audio Feedback  │   │ Caregiver Alert  │
          │    pyttsx3      │   │ Alert Interface  │
          └────────┬────────┘   └────────┬─────────┘
                   │                     │
                   ▼                     ▼
          Audio output layer       Notification layer
Software Components
esp32_cam/

Contains the ESP32-CAM reference firmware.

memoraid_camera.ino provides:

AI Thinker ESP32-CAM configuration
OV2640 camera initialization
Wi-Fi connectivity
JPEG image capture
HTTP endpoints for camera access
Basic device status endpoint

The firmware is intended as the camera acquisition layer of the system.

face_recognition/

Contains the local computer-vision reference pipeline.

recognizer.py

Provides the FaceRecognitionSystem interface.

The current local implementation uses OpenCV's Haar Cascade detector to:

load the face detector
read images
detect faces
return detected face bounding boxes

The current implementation is face detection, not biometric identity recognition.

run_recognition.py

Connects the face-detection module with the audio and caregiver layers.

The pipeline can process an image and generate a structured result when a face is detected.

audio/
audio_feedback.py

Provides the software audio-feedback layer using pyttsx3.

The interface includes responses for events such as:

startup
person detected
unknown person
no person detected

In the local reference implementation, audio is produced through the computer's audio system. The physical prototype's amplifier and bone-conduction speaker represent the corresponding hardware output layer.

caregiver/
caregiver_alert.py

Provides a caregiver-notification interface.

The current reference implementation:

creates structured alert data
records the event type
records a timestamp
optionally records a supplied confidence value
prints the alert for local testing

It does not claim to be connected to a production messaging service.

Local Test Environment

The reference pipeline was tested locally using:

Python 3.12
OpenCV 4.13.0
NumPy
pyttsx3
Flask
Requests
Windows

The dependency versions are listed in:

requirements.txt
Verified Local Tests

The current reference implementation has been tested with a sample image.

Face Detection

Input image:

test_face.jpg

Observed result:

Faces detected: 1
Boxes: [[43, 67, 88, 88]]

A detection-result image was also generated with the detected face highlighted by a bounding box.

Pipeline Test

The image was passed through the reference recognition pipeline and produced:

MEMORAID: Face detected is nearby.

The current fallback returns a detection result rather than a verified identity.

Caregiver Alert Test

The caregiver interface successfully generated a structured event containing:

Event: Unknown person detected
Confidence: 87.0%

The confidence value in this standalone test was manually supplied and is not a measured model confidence.

Current Implementation Status
Component	Status
ESP32-CAM reference firmware	Implemented
OV2640 camera initialization	Implemented
Local face detection	Implemented
Image processing pipeline	Implemented
Audio feedback interface	Implemented
Caregiver alert interface	Implemented
Local end-to-end software test	Verified
Biometric identity recognition	Not implemented in current fallback
Production caregiver messaging	Not implemented
Physical hardware integration test	Requires prototype hardware
Edge-device ML deployment	Future integration
Running the Local Reference Pipeline

Create and activate a Python virtual environment:

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the face-detection module:

cd face_recognition
python recognizer.py

Run the recognition pipeline:

python run_recognition.py

To process an image from Python:

from run_recognition import MemoraidRecognitionPipeline

pipeline = MemoraidRecognitionPipeline()

result = pipeline.process_image(
    r"C:\path\to\image.jpg"
)

print(result)
Future Development

The reference implementation provides a baseline for further development.

Potential next steps include:

Replace the Haar Cascade fallback with a dedicated face-recognition model.
Add reference-face enrollment and identity matching.
Evaluate recognition accuracy using a documented dataset.
Deploy inference closer to the ESP32-CAM edge.
Connect the physical audio amplifier and bone-conduction speaker.
Add a real caregiver notification service.
Add event logging and timestamped incident history.
Evaluate latency, false positives, and false negatives.
Optimize the pipeline for embedded-device constraints.
Repository Structure
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
│   ├── run_recognition.py
│   └── test_face.jpg
│
├── app.py
├── requirements.txt
└── README.md
Development Note

This software directory is intended to make the MEMORAID architecture understandable, testable, and reproducible while clearly separating the reconstructed reference implementation from the original physical prototype.


Then click **Commit changes**.

Use this commit message:

```text
Document MEMORAID software architecture and tests
