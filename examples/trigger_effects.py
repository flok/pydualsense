from pydualsense import *

# get dualsense instance
dualsense = pydualsense()
# set left trigger mode to rigid and put some force values on it
dualsense.setLeftTriggerMode(TriggerModes.Rigid)
dualsense.setLeftTriggerForce(1, 255)
# sleep a little to see the result on the controller
# this is not needed in normal usage
import time; time.sleep(2)
# terminate the thread for message and close the device
dualsense.close()