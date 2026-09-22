Examples
========

The examples ship with the package and can be run from any directory after installation. For example:

.. code-block:: console

   python -m pydualsense.examples --help
   python -m pydualsense.examples read-controller

The command-line modules are ``leds``, ``effects``, ``read_controller``, ``read_all_input_channels``, and ``read_trigger_values``. The source files are also available in the repository's ``examples`` folder.

The following snippets show how the library can be used in your own application.

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

    import time

    with pydualsense() as dualsense:
        dualsense.cross_pressed += cross_down
        dualsense.circle_pressed += circle_down
        dualsense.dpad_down += dpad_down
        dualsense.left_joystick_changed += joystick
        dualsense.gyro_changed += gyro_changed

        while not dualsense.state.R1:
            time.sleep(0.01)


The above example demonstrates the newly added c# like event system that makes it possible to trigger an event for the inputs of the controller.


.. code-block:: python

    from pydualsense import *

    import time

    with pydualsense() as dualsense:
        print('Trigger Effect demo started')
        dualsense.setLeftMotor(255)
        dualsense.setRightMotor(100)
        dualsense.triggerL.setMode(TriggerModes.Rigid)
        dualsense.triggerL.setForce(1, 255)
        dualsense.triggerR.setMode(TriggerModes.Pulse_A)
        dualsense.triggerR.setForce(0, 200)
        dualsense.triggerR.setForce(1, 255)
        dualsense.triggerR.setForce(2, 175)

        while not dualsense.state.R1:
            time.sleep(0.01)
