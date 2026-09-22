import time

from pydualsense import pydualsense


def main() -> None:
    with pydualsense() as dualsense:
        print("Reading controller input channels. Press Ctrl+C to exit.")
        while dualsense.states is None:
            time.sleep(0.05)

        while True:
            states = dualsense.states
            if states is not None:
                print(" ".join(f"{value:03}" for value in states), flush=True)
            time.sleep(0.5)


if __name__ == "__main__":
    main()
