from pydualsense import pydualsense
import time

dualsense = pydualsense()
dualsense.init()


dualsense.triggerR.setEffect('rigid')
dualsense.triggerL.setEffect('rigid')
time.sleep(5)

dualsense.triggerR.setEffect('weapon')
dualsense.triggerL.setEffect('weapon')
time.sleep(5)

dualsense.triggerR.setEffect('vibration')
dualsense.triggerL.setEffect('vibration')
time.sleep(5)

dualsense.triggerR.setEffect('off')
dualsense.triggerL.setEffect('off')
time.sleep(0.5)
dualsense.close()