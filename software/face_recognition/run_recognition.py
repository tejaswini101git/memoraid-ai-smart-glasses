"""
MEMORAID - Recognition Pipeline

Connects:
    Image input
        ↓
    Face recognition
        ↓
    Decision logic
        ↓
    Audio feedback / caregiver alert


"""

import cv2

from recognizer import FaceRecognitionSystem
import sys
from pathlib import Path

SOFTWARE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE_DIR))

from audio.audio_feedback import AudioFeedback
from caregiver.caregiver_alert import CaregiverAlert


class MemoraidRecognitionPipeline:
    """Main recognition and response pipeline."""

    def __init__(self):
        self.recognizer = FaceRecognitionSystem()
        self.audio = AudioFeedback()

        self.caregiver = CaregiverAlert(
            caregiver_name="Primary Caregiver"
        )

    # ---------------------------------------------------------
    # Register known people
    # ---------------------------------------------------------

    def register_person(
        self,
        image_path: str,
        name: str
    ) -> bool:

        return self.recognizer.register_person(
            image_path,
            name
        )

    # ---------------------------------------------------------
    # Process one image
    # ---------------------------------------------------------

    def process_image(
        self,
        image_path: str
    ) -> dict:
        """
        Process an image and trigger the appropriate
        MEMORAID response.
        """

        image = cv2.imread(
            image_path
        )

        if image is None:
            raise FileNotFoundError(
                f"Unable to read image: {image_path}"
            )

        name, confidence = (
            self.recognizer.recognize(
                image
            )
        )

        # -----------------------------------------------------
        # Known person
        # -----------------------------------------------------

        if name is not None:

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


# =============================================================
# Example usage
# =============================================================

if __name__ == "__main__":

    pipeline = MemoraidRecognitionPipeline()

    # ---------------------------------------------------------
    # Register reference faces.
    #
    # Replace these with actual test/reference images when
    # running the reconstructed implementation.
    # ---------------------------------------------------------

    # pipeline.register_person(
    #     "known_faces/caregiver.jpg",
    #     "Caregiver"
    # )

    # ---------------------------------------------------------
    # Process a test image.
    # ---------------------------------------------------------

    # result = pipeline.process_image(
    #     "test_images/test.jpg"
    # )

    # print(result)
