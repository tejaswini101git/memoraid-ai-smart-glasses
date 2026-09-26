"""
MEMORAID - Main Application

Reconstructed/reference implementation based on the
documented MEMORAID architecture.

System flow:

ESP32-CAM / OV2640
        ↓
Image capture
        ↓
Face recognition
        ↓
Decision logic
   ┌────┴────┐
Known       Unknown
  ↓            ↓
Audio       Caregiver
feedback      alert
"""

from pathlib import Path

from face_recognition import FaceRecognitionSystem
from audio.audio_feedback import AudioFeedback
from caregiver.caregiver_alert import CaregiverAlert


# =============================================================
# Configuration
# =============================================================

BASE_DIR = Path(__file__).resolve().parent

KNOWN_FACES_DIR = (
    BASE_DIR / "face_recognition" / "known_faces"
)

TEST_IMAGES_DIR = (
    BASE_DIR / "face_recognition" / "test_images"
)


# =============================================================
# MEMORAID Application
# =============================================================

class MemoraidApp:
    """Main MEMORAID software application."""

    def __init__(self):

        self.recognizer = FaceRecognitionSystem(
            tolerance=0.50
        )

        self.audio = AudioFeedback()

        self.caregiver = CaregiverAlert(
            caregiver_name="Primary Caregiver"
        )

    # ---------------------------------------------------------
    # Load known faces
    # ---------------------------------------------------------

    def load_known_faces(self):
        """
        Load reference face images from the known_faces
        directory.

        Expected format:

        known_faces/
            person1.jpg
            person2.jpg
        """

        if not KNOWN_FACES_DIR.exists():

            print(
                "Known faces directory not found."
            )

            return

        for image_path in KNOWN_FACES_DIR.iterdir():

            if image_path.suffix.lower() not in {
                ".jpg",
                ".jpeg",
                ".png"
            }:
                continue

            person_name = image_path.stem

            success = (
                self.recognizer.register_person(
                    str(image_path),
                    person_name
                )
            )

            if not success:

                print(
                    f"Could not register "
                    f"{person_name}"
                )

    # ---------------------------------------------------------
    # Process image
    # ---------------------------------------------------------

    def process_image(
        self,
        image_path: str
    ):

        print(
            f"\nProcessing image: {image_path}"
        )

        name, confidence = (
            self.recognizer.recognize_image(
                image_path
            )
        )

        # -----------------------------------------------------
        # Known person
        # -----------------------------------------------------

        if name is not None:

            print(
                f"Recognized: {name}"
            )

            print(
                f"Confidence: "
                f"{confidence:.2%}"
            )

            self.audio.person_recognized(
                name
            )

            return {
                "status": "recognized",
                "person": name,
                "confidence": confidence
            }

        # -----------------------------------------------------
        # Unknown person
        # -----------------------------------------------------

        print(
            "Unknown person detected."
        )

        self.audio.unknown_person()

        alert = (
            self.caregiver
            .unknown_person_detected(
                confidence=confidence
            )
        )

        return {
            "status": "unknown",
            "person": None,
            "confidence": confidence,
            "alert": alert
        }

    # ---------------------------------------------------------
    # Start application
    # ---------------------------------------------------------

    def start(self):

        print()
        print("=" * 50)
        print("          MEMORAID AI SYSTEM")
        print("=" * 50)

        print(
            "Initializing recognition system..."
        )

        self.load_known_faces()

        self.audio.startup()

        print(
            "MEMORAID system ready."
        )

        print("=" * 50)


# =============================================================
# Application entry point
# =============================================================

def main():

    app = MemoraidApp()

    app.start()

    print()
    print(
        "Application initialized successfully."
    )


if __name__ == "__main__":
    main()
