from pydualsense import *

# get dualsense instance
dualsense = pydualsense()
dualsense.init()

print('Trigger Effect demo started')

dualsense.setLeftMotor(255)
dualsense.setRightMotor(100)
dualsense.setLeftTriggerMode(TriggerModes.Rigid)
dualsense.setLeftTriggerForce(1, 255)

dualsense.setRightTriggerMode(TriggerModes.Pulse_A)
dualsense.setRightTriggerForce(0, 200)
dualsense.setRightTriggerForce(1, 255)
dualsense.setRightTriggerForce(2, 175)

import time; time.sleep(3)

# terminate the thread for message and close the device
dualsense.close()