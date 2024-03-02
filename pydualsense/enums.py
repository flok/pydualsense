from enum import IntFlag


class ConnectionType(IntFlag):
    BT = 0x0
    USB = 0x1


class LedOptions(IntFlag):
    Off = 0x0
    PlayerLedBrightness = 0x1
    UninterrumpableLed = 0x2
    Both = 0x01 | 0x02


class PulseOptions(IntFlag):
    Off = 0x0
    FadeBlue = 0x1
    FadeOut = 0x2


class Brightness(IntFlag):
    high = 0x0
    medium = 0x1
    low = 0x2


class PlayerID(IntFlag):
    PLAYER_1 = 4
    PLAYER_2 = 10
    PLAYER_3 = 21
    PLAYER_4 = 27
    ALL = 31


class TriggerModes(IntFlag):
    Off = 0x0  # no resistance
    Rigid = 0x1  # continous resistance
    Pulse = 0x2  # section resistance
    Rigid_A = 0x1 | 0x20
    Rigid_B = 0x1 | 0x04
    Rigid_AB = 0x1 | 0x20 | 0x04
    Pulse_A = 0x2 | 0x20
    Pulse_B = 0x2 | 0x04
    Pulse_AB = 0x2 | 0x20 | 0x04
    Calibration = 0xFC


class BatteryState(IntFlag):
    POWER_SUPPLY_STATUS_DISCHARGING = 0x0
    POWER_SUPPLY_STATUS_CHARGING = 0x1
    POWER_SUPPLY_STATUS_FULL = 0x2
    POWER_SUPPLY_STATUS_NOT_CHARGING = 0xB
    POWER_SUPPLY_STATUS_ERROR = 0xF
    POWER_SUPPLY_TEMP_OR_VOLTAGE_OUT_OF_RANGE = 0xA
    POWER_SUPPLY_STATUS_UNKNOWN = 0x0
