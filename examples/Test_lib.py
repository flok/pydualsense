# using new conda environment to chack the new package
import pydualsense as ds
import time

def test_connection():
    controller = ds.pydualsense()

    controller.init()
    for i in range(255):
        controller.setLeftMotor(i)
        time.sleep(0.01)
    
    controller.setLeftMotor(0)

    controller.close()

if __name__ == "__main__":
    test_connection()