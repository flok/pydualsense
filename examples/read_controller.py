from pydualsense import *

# create dualsense
dualsense = pydualsense()
# find device and initialize
dualsense.init()

# read controller state until R1 is pressed
while not dualsense.state.R1:
    print(f"Circle : {dualsense.state.circle} Cross : {dualsense.state.cross} L Stick X : {dualsense.state.LX} L Stick Y : {dualsense.state.LY}")

# close device
dualsense.close()


