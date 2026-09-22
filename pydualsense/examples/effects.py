import time

from pydualsense import TriggerModes, pydualsense


def main() -> None:
    with pydualsense() as dualsense:
        print("Trigger effect demo started. Press R1 to exit.")
        dualsense.setLeftMotor(255)
        dualsense.setRightMotor(100)
        dualsense.triggerL.setMode(TriggerModes.Rigid)
        dualsense.triggerL.setForce(1, 255)

        dualsense.triggerR.setMode(TriggerModes.Pulse_A)
        dualsense.triggerR.setForce(0, 200)
        dualsense.triggerR.setForce(1, 255)
        dualsense.triggerR.setForce(2, 175)

        while not dualsense.state.R1:
            time.sleep(0.01)


if __name__ == "__main__":
    main()
