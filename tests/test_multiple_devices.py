from __future__ import annotations

import sys

from pydualsense import ControllerInfo, discover_devices, pydualsense
from pydualsense.pydualsense import DUALSENSE_PIDS, DUALSENSE_VID

# The class pydualsense shadows the module in this namespace,
# so reach the module through sys.modules to patch hidapi.enumerate.
pds_module = sys.modules["pydualsense.pydualsense"]


class FakeDeviceInfo:
    def __init__(self, product_id: int, serial_number: str | None) -> None:
        self.path = "/dev/fake"
        self.vendor_id = DUALSENSE_VID
        self.product_id = product_id
        self.serial_number = serial_number


def demo() -> None:
    fake_devices = [
        FakeDeviceInfo(0x0CE6, "one"),
        FakeDeviceInfo(0x0CE6, "one"),
        FakeDeviceInfo(0x0DF2, None),
        FakeDeviceInfo(0x0CE6, None),
        FakeDeviceInfo(0x0CE6, "two"),
    ]
    pds_module.hidapi.enumerate = lambda vendor_id: fake_devices

    controllers = discover_devices()
    assert len(controllers) == 4, f"expected 4 controllers, got {len(controllers)}"
    assert [c.serial_number for c in controllers] == ["one", None, None, "two"]
    assert [c.is_edge for c in controllers] == [False, True, False, False]
    assert all(c.interface.vendor_id == DUALSENSE_VID for c in controllers)
    assert all(c.interface.product_id in DUALSENSE_PIDS for c in controllers)

    selected = ControllerInfo(interface=fake_devices[0], serial_number="one", is_edge=False)
    assert selected.interface.path == "/dev/fake"
    assert ControllerInfo(interface=fake_devices[0], serial_number="one", is_edge=False) == selected
    assert pydualsense(device=selected)._device is selected


if __name__ == "__main__":
    demo()
    print("test_multiple_devices: ok")
