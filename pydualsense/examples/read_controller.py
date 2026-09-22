import time

from pydualsense import pydualsense


def cross_down(state: bool) -> None:
    print(f"cross {state}")


def circle_down(state: bool) -> None:
    print(f"circle {state}")


def dpad_down(state: bool) -> None:
    print(f"dpad {state}")


def joystick(state_x: int, state_y: int) -> None:
    print(f"lj {state_x} {state_y}")


def gyro_changed(pitch: int, yaw: int, roll: int) -> None:
    print(f"{pitch}, {yaw}, {roll}")


def main() -> None:
    with pydualsense() as dualsense:
        dualsense.cross_pressed += cross_down
        dualsense.circle_pressed += circle_down
        dualsense.dpad_down += dpad_down
        dualsense.left_joystick_changed += joystick
        dualsense.gyro_changed += gyro_changed

        print("Controller events active. Press R1 to exit.")
        while not dualsense.state.R1:
            time.sleep(0.01)


if __name__ == "__main__":
    main()
