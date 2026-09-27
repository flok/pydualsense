from __future__ import annotations

import os
import sys
import unittest

# run against the working tree copy, not the (older) wheel in site-packages
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydualsense import DSAudio, DSLight, DSState, DSTrigger, Event, pydualsense
from pydualsense.checksum import compute
from pydualsense.enums import BatteryState, ConnectionType
from pydualsense.pydualsense import DSBattery


def _base_report() -> list:
    """64-byte USB report exercising every parsed field."""
    report = [0] * 64
    report[1] = 200       # LX = 72
    report[2] = 134       # LY = 6
    report[3] = 128       # RX = 0
    report[4] = 190       # RY = 62
    report[5] = 128       # L2 pressed, L2_value = 128
    report[6] = 255       # R2 pressed, R2_value = 255
    report[8] = 0x84      # triangle (0x80) + dpad nibble 4 (Down)
    report[9] = 0xFF      # R3, L3, options, share, R2Btn, L2Btn, R1, L1
    report[10] = 0x07     # ps, touch, mic
    report[16], report[17] = 0xD2, 0x04  # accel X = 1234
    report[18], report[19] = 0x2E, 0xFB  # accel Y = -1234
    report[20], report[21] = 0xC4, 0x09  # accel Z = 2500
    report[22], report[23] = 0x2C, 0x01  # gyro Pitch = 300
    report[24], report[25] = 0xD4, 0xFE  # gyro Yaw = -300
    report[26], report[27] = 0xE7, 0x03  # gyro Roll = 999
    report[53] = 0xA4     # battery State = 0xA, Level = 45
    return report


class TestInputParsing(unittest.TestCase):
    def setUp(self) -> None:
        self.ds = pydualsense()  # no init(), no HID device needed
        self.ds.conType = ConnectionType.USB
        self.ds.is_edge = False
        self.ds.state = DSState()
        self.ds.battery = DSBattery()

    def test_usb_input_parsing(self) -> None:
        report = _base_report()

        # first call sets state and last_states, fires no events
        self.ds.readInput(report)
        self.assertIsNotNone(self.ds.last_states)
        self.assertEqual(self.ds._event_queue.qsize(), 0)

        self.assertEqual(self.ds.state.LX, 72)
        self.assertEqual(self.ds.state.LY, 6)
        self.assertEqual(self.ds.state.RX, 0)
        self.assertEqual(self.ds.state.RY, 62)
        self.assertIs(self.ds.state.L2, True)
        self.assertIs(self.ds.state.R2, True)
        self.assertEqual(self.ds.state.L2_value, 128)
        self.assertEqual(self.ds.state.R2_value, 255)

        self.assertIs(self.ds.state.triangle, True)
        self.assertIs(self.ds.state.circle, False)
        self.assertIs(self.ds.state.cross, False)
        self.assertIs(self.ds.state.square, False)

        # dpad nibble 4 -> Down only
        self.assertEqual(
            (
                self.ds.state.DpadUp,
                self.ds.state.DpadDown,
                self.ds.state.DpadLeft,
                self.ds.state.DpadRight,
            ),
            (False, True, False, False),
        )

        self.assertEqual(
            (
                self.ds.state.R3,
                self.ds.state.L3,
                self.ds.state.options,
                self.ds.state.share,
                self.ds.state.R2Btn,
                self.ds.state.L2Btn,
                self.ds.state.R1,
                self.ds.state.L1,
            ),
            (True,) * 8,
        )

        self.assertIs(self.ds.state.ps, True)
        self.assertIs(self.ds.state.touchBtn, True)
        self.assertIs(self.ds.state.micBtn, True)
        self.assertIsNone(self.ds.state.L4)  # non-edge leaves edge buttons unset

        self.assertEqual(self.ds.battery.State, BatteryState(0xA))
        self.assertEqual(self.ds.battery.Level, 45)

        self.assertEqual(
            (
                self.ds.state.accelerometer.X,
                self.ds.state.accelerometer.Y,
                self.ds.state.accelerometer.Z,
            ),
            (1234, -1234, 2500),
        )
        self.assertEqual(
            (
                self.ds.state.gyro.Pitch,
                self.ds.state.gyro.Yaw,
                self.ds.state.gyro.Roll,
            ),
            (300, -300, 999),
        )

    def test_dpad_changed_event(self) -> None:
        base = _base_report()  # dpad nibble 4 (Down)
        up = list(base)
        up[8] = 0x80  # triangle held, dpad 0 = Up

        # first call sets last_states, fires no events
        self.ds.readInput(base)

        seen: list = []

        def recorder(event, handlers, args, kwargs):
            seen.append(kwargs)

        orig = self.ds.dpad_changed._dispatcher
        self.ds.dpad_changed._dispatcher = recorder
        try:
            self.ds.readInput(up)
        finally:
            self.ds.dpad_changed._dispatcher = orig

        self.assertEqual(len(seen), 1)
        self.assertEqual(seen, [{"up": True, "down": False, "left": False, "right": False}])

    def test_button_bool_event(self) -> None:
        base = _base_report()
        held = list(base)
        held[8] = 0x80  # triangle held, dpad Up
        released = list(held)
        released[8] = 0  # triangle released, dpad unchanged (Up)

        # two reads so last_states holds (triangle held, dpad Up) before the release
        self.ds.readInput(base)
        self.ds.readInput(held)

        seen: list = []

        def recorder(event, handlers, args, kwargs):
            seen.append(args)

        orig = self.ds.triangle_pressed._dispatcher
        self.ds.triangle_pressed._dispatcher = recorder
        try:
            self.ds.readInput(released)
        finally:
            self.ds.triangle_pressed._dispatcher = orig

        self.assertEqual(seen, [(False,)])
        self.assertIsInstance(seen[0][0], bool)

    def test_bt_report_crc(self) -> None:
        ds_bt = pydualsense()
        ds_bt.conType = ConnectionType.BT
        ds_bt.output_report_length = 78
        ds_bt.audio = DSAudio()
        ds_bt.triggerL = DSTrigger()
        ds_bt.triggerR = DSTrigger()
        ds_bt.light = DSLight()
        out_report = ds_bt.prepareReport()
        self.assertIsInstance(out_report, list)
        self.assertEqual(len(out_report), 78)
        self.assertEqual(out_report[0], ds_bt.OUTPUT_REPORT_BT)
        crc = compute(out_report)
        self.assertEqual(
            out_report[74:78],
            [
                crc & 0x000000FF,
                (crc & 0x0000FF00) >> 8,
                (crc & 0x00FF0000) >> 16,
                (crc & 0xFF000000) >> 24,
            ],
        )

    def test_coalesce(self) -> None:
        while not self.ds._event_queue.empty():
            self.ds._event_queue.get_nowait()

        ev = Event(coalesce=True)
        self.ds._queue_event(ev, [], (1,), {})
        self.ds._queue_event(ev, [], (2,), {})
        self.assertEqual(self.ds._coalesce_pending[ev], ((2,), {}))
        self.assertIn(ev, self.ds._coalesce_inqueue)
        self.assertEqual(self.ds._event_queue.qsize(), 1)
        self.assertIsInstance(self.ds._event_queue.get_nowait(), Event)
        self.assertTrue(self.ds._event_queue.empty())

    def test_dropped_events_zero(self) -> None:
        self.assertEqual(self.ds.dropped_events, 0)


if __name__ == "__main__":
    unittest.main()
