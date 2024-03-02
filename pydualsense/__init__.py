import os
import sys
sys.path.append(os.path.dirname(__file__))

from .enums import LedOptions, Brightness, PlayerID, PulseOptions, TriggerModes # noqa : F401
from .event_system import Event # noqa : F401
from .pydualsense import pydualsense, DSLight, DSState, DSTouchpad, DSTrigger, DSAudio # noqa : F401

__version__ = "0.7.1"