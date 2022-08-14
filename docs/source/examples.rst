Examples
========

This pages displays some examples that on how the library can be used. All the examples can also be found inside the `examples` folder on the github repository.

.. code-block:: python

    from pydualsense import *

    def cross_down(state):
        print(f'cross {state}')


    def circle_down(state):
        print(f'circle {state}')


    def dpad_down(state):
        print(f'dpad down {state}')


    def joystick(stateX, stateY):
        print(f'joystick {stateX} {stateY}')


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


The above example demonstrates the newly added c# like event system that makes it possible to trigger an event for the inputs of the controller.


.. code-block:: python

    from pydualsense import *

    # get dualsense instance
    dualsense = pydualsense()
    # initialize controller and connect
    dualsense.init()

    print('Trigger Effect demo started')

    # set left and right rumble motors
    dualsense.setLeftMotor(255)
    dualsense.setRightMotor(100)

    # set left l2 trigger to Rigid and set index 1 to force 255
    dualsense.triggerL.setMode(TriggerModes.Rigid)
    dualsense.triggerL.setForce(1, 255)

    # set left r2 trigger to Rigid
    dualsense.triggerR.setMode(TriggerModes.Pulse_A)
    dualsense.triggerR.setForce(0, 200)
    dualsense.triggerR.setForce(1, 255)
    dualsense.triggerR.setForce(2, 175)

    # loop until r1 is pressed to feel effect
    while not dualsense.state.R1:
        ...

    # terminate the thread for message and close the device
    dualsense.close()