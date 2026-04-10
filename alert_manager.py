"""Desktop notification and sound alert management."""

from plyer import notification
import time
from playsound import playsound
import threading

import config


def play_sound():
    """Play the configured alert sound for the configured duration."""

    start = time.time()

    while time.time() - start < config.SOUND_DURATION_SECONDS:
        playsound(config.ALERT_SOUND_PATH)


def send_alert(symbol, zone_name):
    """Send a desktop notification and play an alert sound asynchronously.

    Args:
        symbol (str): The MetaTrader symbol name that triggered the alert.
        zone_name (str): The textual name of the zone that is near the price.
    """

    notification.notify(
        title="Zone Alert",
        message=(
            f"{symbol}\n"
            f"Near {zone_name}"
        ),
        timeout=10
    )

    # Play sound in a separate thread so the UI update is not blocked.
    threading.Thread(target=play_sound).start()
