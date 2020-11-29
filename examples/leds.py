from pydualsense import *

# get dualsense instance
dualsense = pydualsense()
# set color around touchpad to red
dualsense.setColor(0,0,255)
# enable microphone indicator
dualsense.setMicrophoneLED(1)
# set all player indicators on
dualsense.setPlayer(PlayerID.all)
# sleep a little to see the result on the controller
# this is not needed in normal usage
import time; time.sleep(2)
# terminate the thread for message and close the device
dualsense.close()