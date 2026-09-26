"""
MEMORAID - Audio Feedback Module



Hardware output:
    Audio amplifier -> Bone conduction speaker

This module converts recognition events into short
spoken feedback messages.
"""

import platform
import subprocess
from typing import Optional


class AudioFeedback:
    """Generate spoken feedback for MEMORAID."""

    def __init__(self, rate: int = 160):
        self.rate = rate

        try:
            import pyttsx3

            self.engine = pyttsx3.init()

            self.engine.setProperty(
                "rate",
                self.rate
            )

        except Exception as error:

            print(
                f"Audio engine initialization warning: {error}"
            )

            self.engine = None

    # ---------------------------------------------------------
    # Speak a message
    # ---------------------------------------------------------

    def speak(self, message: str) -> None:
        """
        Speak a message through the connected audio output.

        On the physical MEMORAID prototype, the audio output
        is intended to reach the amplifier and
        bone-conduction speaker.
        """

        if not message:
            return

        print(
            f"MEMORAID: {message}"
        )

        if self.engine is None:
            return

        try:

            self.engine.say(
                message
            )

            self.engine.runAndWait()

        except Exception as error:

            print(
                f"Audio playback error: {error}"
            )

    # ---------------------------------------------------------
    # Recognition feedback
    # ---------------------------------------------------------

    def person_recognized(
        self,
        name: str
    ) -> None:
        """
        Provide feedback when a known person is recognized.
        """

        self.speak(
            f"{name} is nearby."
        )

    # ---------------------------------------------------------
    # Unknown person feedback
    # ---------------------------------------------------------

    def unknown_person(self) -> None:
        """
        Provide feedback when an unknown person is detected.
        """

        self.speak(
            "An unknown person is nearby."
        )

    # ---------------------------------------------------------
    # No face detected
    # ---------------------------------------------------------

    def no_person_detected(self) -> None:
        """
        Feedback for frames where no face is detected.
        """

        self.speak(
            "No person detected."
        )

    # ---------------------------------------------------------
    # System startup message
    # ---------------------------------------------------------

    def startup(self) -> None:
        """
        Announce MEMORAID system startup.
        """

        self.speak(
            "MEMORAID is ready."
        )


# =============================================================
# Example usage
# =============================================================

if __name__ == "__main__":

    audio = AudioFeedback()

    audio.startup()

    audio.person_recognized(
        "Caregiver"
    )

    audio.unknown_person()
