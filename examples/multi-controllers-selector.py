from pydualsense import *

import time

# get dualsense instance
dualsense = pydualsense()
dualsense.init()

dualsense.setController.choose(0) # choose controller 1
time.sleep(0.01) # sleep a little to see the result on the controller
dualsense.light.setColorI(0, 255, 0) # set color around touchpad to red
dualsense.light.setPlayerID(PlayerID.PLAYER_1) # set all player 1 indicator on
time.sleep(2) # sleep a little to see the result on the controller, this is not needed in normal usage

dualsense.setController.choose(1) # choose controller 2
time.sleep(0.01)
dualsense.light.setColorI(255, 0, 0)# set color around touchpad to green
dualsense.light.setPlayerID(PlayerID.PLAYER_2) # set all player 2 indicator on
time.sleep(2)

dualsense.close() # terminate the thread for message and close the device