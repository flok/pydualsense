from pydualsense import *
import time

dualsense = pydualsense()
dualsense.init()


dualsense.triggerR.setEffect(TriggersEffects.RIGID)
dualsense.triggerL.setEffect(TriggersEffects.RIGID)
time.sleep(5)

dualsense.triggerR.setEffect(TriggersEffects.WEAPON)
dualsense.triggerL.setEffect(TriggersEffects.WEAPON)
time.sleep(5)

dualsense.triggerR.setEffect(TriggersEffects.VIBRATION)
dualsense.triggerL.setEffect(TriggersEffects.VIBRATION)
time.sleep(5)

dualsense.triggerR.setEffect(TriggersEffects.OFF)
dualsense.triggerL.setEffect(TriggersEffects.OFF)
time.sleep(0.5)
dualsense.close()