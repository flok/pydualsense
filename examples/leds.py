from pydualsense import *

# get dualsense instance
dualsense = pydualsense()
dualsense.init()
# set color around touchpad to red
dualsense.light.setColorI(255,0,0)
# mute microphone
dualsense.audio.setMicrophoneState(True)
# set all player 1 indicator on
dualsense.light.setPlayerID(PlayerID.player1)
# sleep a little to see the result on the controller
# this is not needed in normal usage
import time; time.sleep(2)
# terminate the thread for message and close the device
dualsense.close()