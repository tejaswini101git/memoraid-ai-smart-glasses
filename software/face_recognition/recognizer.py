"""
MEMORAID - Face Detection and Recognition Module



This local version uses OpenCV's Haar Cascade detector so that
the pipeline can be tested without the dlib dependency.
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class FaceRecognitionSystem:
    """Face detection/recognition interface for MEMORAID."""

    def __init__(self):
        cascade_path = cv2.data.haarcascades + (
            "haarcascade_frontalface_default.xml"
        )

        self.face_detector = cv2.CascadeClassifier(
            cascade_path
        )

        if self.face_detector.empty():
            raise RuntimeError(
                "Unable to load OpenCV face detector."
            )

        # Reference faces can be added later.
        self.known_faces = {}

    # ---------------------------------------------------------
    # Register a reference face
    # ---------------------------------------------------------

    def register_person(
        self,
        image_path: str,
        person_name: str
    ) -> bool:
        """
        Store a reference image for a known person.

        Note:
        This lightweight local implementation performs face
        detection. It does not claim biometric identification
        accuracy comparable to a dedicated recognition model.
        """

        image = cv2.imread(image_path)

        if image is None:
            print(
                f"Unable to read image: {image_path}"
            )
            return False

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        if len(faces) == 0:
            print(
                f"No face detected in {image_path}"
            )
            return False

        self.known_faces[person_name] = image

        print(
            f"Registered reference image for: "
            f"{person_name}"
        )

        return True

    # ---------------------------------------------------------
    # Detect faces
    # ---------------------------------------------------------

    def detect_faces(
        self,
        image: np.ndarray
    ):
        """Detect faces in an OpenCV image."""

        if image is None:
            return []

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60)
        )

        return faces

    # ---------------------------------------------------------
    # Process image
    # ---------------------------------------------------------

    def recognize(
        self,
        image: np.ndarray
    ) -> Tuple[Optional[str], float]:
        """
        Detect a face and return the current recognition result.

        The local fallback identifies the presence of a face,
        while a dedicated recognition model can be integrated
        later.
        """

        faces = self.detect_faces(image)

        if len(faces) == 0:
            return None, 0.0

        # For this local reference implementation, detection
        # confidence is represented as a simple availability
        # signal rather than a biometric confidence score.
        return "Face detected", 1.0

    # ---------------------------------------------------------
    # Process image file
    # ---------------------------------------------------------

    def recognize_image(
        self,
        image_path: str
    ) -> Tuple[Optional[str], float]:
        """Process an image file."""

        image = cv2.imread(
            image_path
        )

        if image is None:
            raise FileNotFoundError(
                f"Unable to read image: {image_path}"
            )

        return self.recognize(
            image
        )


# =============================================================
# Local test
# =============================================================

if __name__ == "__main__":

    recognizer = FaceRecognitionSystem()

    print(
        "MEMORAID face detection module initialized."
    )
