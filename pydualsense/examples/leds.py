import time

from pydualsense import pydualsense
from pydualsense.enums import PlayerID


def main() -> None:
    with pydualsense() as dualsense:
        dualsense.light.setColorI(255, 0, 0)
        dualsense.audio.setMicrophoneState(True)
        dualsense.light.setPlayerID(PlayerID.PLAYER_1)
        time.sleep(2)


if __name__ == "__main__":
    main()
