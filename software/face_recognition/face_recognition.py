"""
MEMORAID - Face Recognition Module

Reconstructed/reference implementation based on the
documented MEMORAID system architecture.

Input:
    Image/frame captured from the ESP32-CAM.

Output:
    Recognized person name and confidence.

This module can be connected to the ESP32-CAM capture
endpoint or used independently with a local image.
"""

import cv2
import numpy as np
import face_recognition
from typing import Optional, Tuple


class FaceRecognitionSystem:
    """Face recognition engine for MEMORAID."""

    def __init__(self, tolerance: float = 0.50):
        self.tolerance = tolerance

        self.known_encodings = []
        self.known_names = []

    # ---------------------------------------------------------
    # Register a known person
    # ---------------------------------------------------------

    def register_person(
        self,
        image_path: str,
        person_name: str
    ) -> bool:
        """
        Register a person's face from an image.

        Parameters
        ----------
        image_path : str
            Path to the person's reference image.

        person_name : str
            Name associated with the face.

        Returns
        -------
        bool
            True if a face was successfully registered.
        """

        image = face_recognition.load_image_file(
            image_path
        )

        encodings = face_recognition.face_encodings(
            image
        )

        if not encodings:
            print(
                f"No face detected in {image_path}"
            )
            return False

        self.known_encodings.append(
            encodings[0]
        )

        self.known_names.append(
            person_name
        )

        print(
            f"Registered person: {person_name}"
        )

        return True

    # ---------------------------------------------------------
    # Recognize a face from an image
    # ---------------------------------------------------------

    def recognize(
        self,
        image: np.ndarray
    ) -> Tuple[Optional[str], float]:
        """
        Detect and recognize the most relevant face.

        Parameters
        ----------
        image : numpy.ndarray
            BGR image from OpenCV.

        Returns
        -------
        tuple
            (person_name, confidence)

            person_name = None when no known face is found.
        """

        if image is None:
            return None, 0.0

        # OpenCV uses BGR while face_recognition expects RGB.
        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        face_locations = (
            face_recognition.face_locations(
                rgb_image
            )
        )

        if not face_locations:
            return None, 0.0

        face_encodings = (
            face_recognition.face_encodings(
                rgb_image,
                face_locations
            )
        )

        best_name = None
        best_confidence = 0.0

        for face_encoding in face_encodings:

            if not self.known_encodings:
                continue

            distances = (
                face_recognition.face_distance(
                    self.known_encodings,
                    face_encoding
                )
            )

            best_index = int(
                np.argmin(distances)
            )

            best_distance = float(
                distances[best_index]
            )

            # Convert distance into an approximate
            # similarity score.
            confidence = max(
                0.0,
                1.0 - best_distance
            )

            if (
                best_distance <= self.tolerance
                and confidence > best_confidence
            ):

                best_name = (
                    self.known_names[best_index]
                )

                best_confidence = confidence

        return (
            best_name,
            best_confidence
        )

    # ---------------------------------------------------------
    # Process an image file
    # ---------------------------------------------------------

    def recognize_image(
        self,
        image_path: str
    ) -> Tuple[Optional[str], float]:
        """
        Recognize a person from an image file.
        """

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
# Example usage
# =============================================================

if __name__ == "__main__":

    recognizer = FaceRecognitionSystem(
        tolerance=0.50
    )

    # ---------------------------------------------------------
    # Register known people.
    #
    # Replace these paths with your own reference images
    # when actually running the system.
    # ---------------------------------------------------------

    # recognizer.register_person(
    #     "known_faces/caregiver.jpg",
    #     "Caregiver"
    # )

    # ---------------------------------------------------------
    # Test recognition
    # ---------------------------------------------------------

    # name, confidence = recognizer.recognize_image(
    #     "test_images/test.jpg"
    # )

    # if name:
    #     print(
    #         f"Recognized: {name} "
    #         f"({confidence:.2%})"
    #     )
    # else:
    #     print("Unknown person or no face detected.")
