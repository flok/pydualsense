import os
import sys

sys.path.append(os.path.dirname(__file__))

from .enums import Brightness, LedOptions, PlayerID, PulseOptions, TriggerEffects, TriggerModes
from .event_system import Event
from .pydualsense import (
    ControllerInfo,
    DSAudio,
    DSLight,
    DSState,
    DSTouchpad,
    DSTrigger,
    HIDGuardianError,
    NoDeviceError,
    PydualsenseError,
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
    "HIDGuardianError",
    "LedOptions",
    "NoDeviceError",
    "PlayerID",
    "PulseOptions",
    "PydualsenseError",
    "TriggerEffects",
    "TriggerModes",
    "__version__",
    "discover_devices",
    "pydualsense",
]

