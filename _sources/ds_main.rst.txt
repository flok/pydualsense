pydualsense main class
======================

The `pydualsense` class is the core interface for the DualSense controller. It provides comprehensive control and monitoring of all controller features.

Features
--------
- Button state monitoring (triangle, circle, cross, square)
- D-pad control
- Trigger control with analog values
- Touchpad input handling
- Motion sensors (gyroscope and accelerometer)
- LED control and customization
- Audio control
- Battery monitoring
- Event-based input handling

Initialization
-------------
.. code-block:: python

    from pydualsense import pydualsense

    # Create controller instance
    ds = pydualsense()
    
    # Initialize connection
    ds.init()

Core Properties
--------------
- :attr:`state` - Current state of all controller inputs
- :attr:`light` - LED control interface
- :attr:`audio` - Audio control interface
- :attr:`triggerL` - Left trigger control
- :attr:`triggerR` - Right trigger control
- :attr:`battery` - Battery status information

State Properties
---------------
- :attr:`state.square` - Square button state
- :attr:`state.triangle` - Triangle button state
- :attr:`state.circle` - Circle button state
- :attr:`state.cross` - Cross button state
- :attr:`state.L1`, :attr:`state.R1` - L1/R1 button states
- :attr:`state.L2`, :attr:`state.R2` - L2/R2 button states
- :attr:`state.L3`, :attr:`state.R3` - L3/R3 button states
- :attr:`state.DpadUp`, :attr:`state.DpadDown` - D-pad states
- :attr:`state.DpadLeft`, :attr:`state.DpadRight` - D-pad states
- :attr:`state.LX`, :attr:`state.LY` - Left joystick position
- :attr:`state.RX`, :attr:`state.RY` - Right joystick position
- :attr:`state.L1_value`, :attr:`state.R1_value` - Trigger analog values (0-255)
- :attr:`state.L2_value`, :attr:`state.R2_value` - Trigger analog values (0-255)
- :attr:`state.trackPadTouch0`, :attr:`state.trackPadTouch1` - Touchpad touch data
- :attr:`state.gyro` - Gyroscope data (Pitch, Yaw, Roll)
- :attr:`state.accelerometer` - Accelerometer data (X, Y, Z)

Event System
-----------
The controller provides an event-based system for monitoring input changes:

Button Events
~~~~~~~~~~~~
- :attr:`triangle_pressed` - Triangle button state changes
- :attr:`circle_pressed` - Circle button state changes
- :attr:`cross_pressed` - Cross button state changes
- :attr:`square_pressed` - Square button state changes

D-pad Events
~~~~~~~~~~~
- :attr:`dpad_up` - D-pad up state changes
- :attr:`dpad_down` - D-pad down state changes
- :attr:`dpad_left` - D-pad left state changes
- :attr:`dpad_right` - D-pad right state changes

Trigger Events
~~~~~~~~~~~~~
- :attr:`l1_changed` - L1 button state changes
- :attr:`l2_changed` - L2 button state changes
- :attr:`l3_changed` - L3 button state changes
- :attr:`r1_changed` - R1 button state changes
- :attr:`r2_changed` - R2 button state changes
- :attr:`r3_changed` - R3 button state changes
- :attr:`l2_value_changed` - Left trigger analog value changes
- :attr:`r2_value_changed` - Right trigger analog value changes

Motion Events
~~~~~~~~~~~~
- :attr:`gyro_changed` - Gyroscope data changes
- :attr:`accelerometer_changed` - Accelerometer data changes

Joystick Events
~~~~~~~~~~~~~~
- :attr:`left_joystick_changed` - Left joystick position changes
- :attr:`right_joystick_changed` - Right joystick position changes

Other Events
~~~~~~~~~~~
- :attr:`ps_pressed` - PS button state changes
- :attr:`touch_pressed` - Touchpad button state changes
- :attr:`microphone_pressed` - Microphone button state changes
- :attr:`share_pressed` - Share button state changes
- :attr:`option_pressed` - Options button state changes

Examples
--------
Basic Usage
~~~~~~~~~~
.. code-block:: python

    from pydualsense import pydualsense

    # Initialize controller
    ds = pydualsense()
    ds.init()

    # Read button states
    if ds.state.circle:
        print("Circle button is pressed")

    # Read trigger analog values
    print(f"L2 value: {ds.state.L2_value}")
    print(f"R2 value: {ds.state.R2_value}")

    # Read motion data
    print(f"Gyro: P={ds.state.gyro.Pitch}, Y={ds.state.gyro.Yaw}, R={ds.state.gyro.Roll}")
    print(f"Accel: X={ds.state.accelerometer.X}, Y={ds.state.accelerometer.Y}, Z={ds.state.accelerometer.Z}")

Event Handling
~~~~~~~~~~~~~
.. code-block:: python

    # Monitor button presses
    def on_circle_pressed(state):
        print(f"Circle button {'pressed' if state else 'released'}")

    ds.circle_pressed += on_circle_pressed

    # Monitor trigger analog values
    def on_l2_value_changed(value):
        print(f"L2 trigger value: {value}")

    ds.l2_value_changed += on_l2_value_changed

    # Monitor motion data
    def on_gyro_changed(pitch, yaw, roll):
        print(f"Gyro: P={pitch}, Y={yaw}, R={roll}")

    ds.gyro_changed += on_gyro_changed

Error Handling
-------------
The class handles various error conditions:

- Connection errors when controller is not found
- Invalid parameter values for motor intensity, colors, etc.
- Type errors for incorrect parameter types

API Reference
------------
.. automodule:: pydualsense.pydualsense
   :members:
   :undoc-members:
   :show-inheritance: