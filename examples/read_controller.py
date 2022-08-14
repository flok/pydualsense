from pydualsense import *


def cross_down(state):
    print(f'cross {state}')


def circle_down(state):
    print(f'circle {state}')


def dpad_down(state):
    print(f'dpad {state}')


def joystick(stateX, stateY):
    print(f'lj {stateX} {stateY}')


def gyro_changed(pitch, yaw, roll):
    print(f'{pitch}, {yaw}, {roll}')


# create dualsense
dualsense = pydualsense()
# find device and initialize
dualsense.init()

# add events handler functions
dualsense.cross_pressed += cross_down
dualsense.circle_pressed += circle_down
dualsense.dpad_down += dpad_down
dualsense.left_joystick_changed += joystick
dualsense.gyro_changed += gyro_changed

# read controller state until R1 is pressed
while not dualsense.state.R1:
    ...

# close device
dualsense.close()
