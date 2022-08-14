from pydualsense import *

# get dualsense instance
dualsense = pydualsense()
dualsense.init()

print('Trigger Effect demo started')

dualsense.setLeftMotor(255)
dualsense.setRightMotor(100)
dualsense.triggerL.setMode(TriggerModes.Rigid)
dualsense.triggerL.setForce(1, 255)

dualsense.triggerR.setMode(TriggerModes.Pulse_A)
dualsense.triggerR.setForce(0, 200)
dualsense.triggerR.setForce(1, 255)
dualsense.triggerR.setForce(2, 175)

# loop until r1 is pressed to feel effect
while not dualsense.state.R1:
    ...
# terminate the thread for message and close the device
dualsense.close()