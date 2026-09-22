# using new conda environment to chack the new package
import time

import pydualsense as ds
from pydualsense.enums import ConnectionType


def main() -> None:
    with ds.pydualsense() as controller:
        connection_type = "Bluetooth" if controller.conType == ConnectionType.BT else "USB"
        print(f"Controller connected via {connection_type}")

        start_time = time.time()
        print('Press L2 and R2 to see the analog values for 30 seconds, values range from 0 to 255')
        while time.time() - start_time < 30:
            print(f"L2: {controller.state.L2_value} R2: {controller.state.R2_value}", end='\r')
            time.sleep(0.1)

if __name__ == "__main__":
    main()
