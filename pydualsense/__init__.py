import os
import sys

sys.path.append(os.path.dirname(__file__))

from .enums import Brightness, LedOptions, PlayerID, PulseOptions, TriggerModes
from .event_system import Event
from .pydualsense import (
    ControllerInfo,
    DSAudio,
    DSLight,
    DSState,
    DSTouchpad,
    DSTrigger,
    discover_devices,
    pydualsense,
)

__version__ = "0.7.5"

__all__ = [
    "Brightness",
    "ControllerInfo",
    "DSAudio",
    "DSLight",
    "DSState",
    "DSTouchpad",
    "DSTrigger",
    "Event",
    "LedOptions",
    "PlayerID",
    "PulseOptions",
    "TriggerModes",
    "__version__",
    "discover_devices",
    "pydualsense",
]

