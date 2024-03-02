import winreg
import sys


def check_hide() -> bool:
    """
    check if hidguardian is used and controller is hidden
    """
    if sys.platform.startswith("win32"):
        try:
            access_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            access_key = winreg.OpenKey(
                access_reg,
                r"SYSTEM\CurrentControlSet\Services\HidGuardian\Parameters",
                0,
                winreg.KEY_READ,
            )
            affected_devices = winreg.QueryValueEx(access_key, "AffectedDevices")[0]
            if "054C" in affected_devices and "0CE6" in affected_devices:
                return True
            return False
        except OSError:
            pass

    return False
