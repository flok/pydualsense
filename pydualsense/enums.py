from enum import IntFlag


class ConnectionType(IntFlag):
    """
    How the DualSense controller is connected to the computer.
    """

    BT = 0x0,
    USB = 0x1


class LedOptions(IntFlag):
    Off = 0x0,
    PlayerLedBrightness = 0x1,
    UninterrumpableLed = 0x2,
    Both = 0x01 | 0x02


class PulseOptions(IntFlag):
    Off = 0x0,
    FadeBlue = 0x1,
    FadeOut = 0x2


class Brightness(IntFlag):
    high = 0x0,
    medium = 0x1,
    low = 0x2


class PlayerID(IntFlag):
    """
    Possible player id LED states.
    """

    OFF = 0
    PLAYER_1 = 4
    PLAYER_2 = 10
    PLAYER_3 = 21
    PLAYER_4 = 27
    ON = 31


class TriggerModeFlag(IntFlag):
    """
    Known trigger mode flags.
    """

    OFF = 0x00
    RIGID = 0x01
    PULSE = 0x02
    A = 0x20
    B = 0x04
    CALIBRATION = 0xFC
