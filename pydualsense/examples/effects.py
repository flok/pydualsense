import time

from pydualsense import pydualsense, TriggerEffects


def main() -> None:
    with pydualsense() as dualsense:
        print("Trigger effect demo started. Press R1 to exit.")
        dualsense.setLeftMotor(255)
        dualsense.setRightMotor(100)
        dualsense.triggerL.set_effect(TriggerEffects.Soft)
        dualsense.triggerR.set_effect(TriggerEffects.Bow)

        while not dualsense.state.R1:
            time.sleep(0.01)


if __name__ == "__main__":
    main()
