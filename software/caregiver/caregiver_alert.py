"""
MEMORAID - Caregiver Alert Module

Reconstructed/reference implementation based on the
documented MEMORAID system architecture.

Purpose:
    Provide a software interface for sending caregiver
    notifications when an important event is detected.

The notification mechanism is intentionally configurable.
"""

from datetime import datetime
from typing import Optional


class CaregiverAlert:
    """Manage caregiver notifications."""

    def __init__(
        self,
        caregiver_name: str = "Caregiver"
    ):
        self.caregiver_name = caregiver_name

    # ---------------------------------------------------------
    # Create an alert
    # ---------------------------------------------------------

    def create_alert(
        self,
        event: str,
        confidence: Optional[float] = None
    ) -> dict:
        """
        Create a structured caregiver alert.

        Parameters
        ----------
        event : str
            Description of the detected event.

        confidence : float, optional
            Recognition confidence if available.

        Returns
        -------
        dict
            Structured alert information.
        """

        alert = {
            "recipient": self.caregiver_name,
            "event": event,
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            )
        }

        if confidence is not None:

            alert["confidence"] = round(
                float(confidence),
                3
            )

        return alert

    # ---------------------------------------------------------
    # Send alert
    # ---------------------------------------------------------

    def send_alert(
        self,
        event: str,
        confidence: Optional[float] = None
    ) -> dict:
        """
        Generate and log a caregiver alert.

        This reference implementation does not claim to
        connect to a real messaging service.
        """

        alert = self.create_alert(
            event,
            confidence
        )

        print(
            "\n===== MEMORAID CAREGIVER ALERT ====="
        )

        print(
            f"To: {alert['recipient']}"
        )

        print(
            f"Event: {alert['event']}"
        )

        print(
            f"Time: {alert['timestamp']}"
        )

        if "confidence" in alert:

            print(
                f"Confidence: "
                f"{alert['confidence']:.1%}"
            )

        print(
            "====================================\n"
        )

        return alert

    # ---------------------------------------------------------
    # Unknown person alert
    # ---------------------------------------------------------

    def unknown_person_detected(
        self,
        confidence: Optional[float] = None
    ) -> dict:
        """
        Generate an alert for an unknown person.
        """

        return self.send_alert(
            event="Unknown person detected",
            confidence=confidence
        )

    # ---------------------------------------------------------
    # Emergency event
    # ---------------------------------------------------------

    def emergency_event(
        self,
        description: str
    ) -> dict:
        """
        Generate an emergency caregiver alert.
        """

        return self.send_alert(
            event=f"Emergency event: {description}"
        )


# =============================================================
# Example usage
# =============================================================

if __name__ == "__main__":

    caregiver = CaregiverAlert(
        caregiver_name="Primary Caregiver"
    )

    caregiver.unknown_person_detected(
        confidence=0.82
    )

    caregiver.emergency_event(
        "Assistance required"
    )
