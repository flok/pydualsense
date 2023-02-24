# pydualsense
control your dualsense through python. using the hid library this package implements the report features for controlling your PS5 controller.

# Documentation

You can find the documentation at [docs](https://flok.github.io/pydualsense/)

# Installation


## Windows 
Download [hidapi](https://github.com/libusb/hidapi/releases) and place the x64 .dll file into your Workspace. After that install the package from [pypi](https://pypi.org/project/pydualsense/). 

```bash
pip install --upgrade pydualsense
```

## Linux

On Linux based system you first need to add a udev rule to let the user access the PS5 controller without requiring root privileges.

```bash
sudo cp 70-ps5-controller.rules /etc/udev/rules.d
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Then install the hidapi through your package manager of your system.

On an Ubuntu system the package ```libhidapi-dev``` is required.

```bash
sudo apt install libhidapi-dev
```

After that install the package from [pypi](https://pypi.org/project/pydualsense/). 

```bash
pip install --upgrade pydualsense
```

# usage

```python

from pydualsense import pydualsense, TriggerModes

def cross_pressed(state):
    print(state)

ds = pydualsense() # open controller
ds.init() # initialize controller

ds.cross_pressed += cross_pressed
ds.light.setColorI(255,0,0) # set touchpad color to red
ds.triggerL.setMode(TriggerModes.Rigid)
ds.triggerL.setForce(1, 255)
ds.close() # closing the controller
```

See [examples](https://github.com/flok/pydualsense/tree/master/examples) or [examples docs](https://flok.github.io/pydualsense/examples.html) folder for some more ideas

# Help wanted

Help wanted from people that want to use this and have feature requests. Just open a issue with the correct label.

# dependecies

- hidapi-usb >= 0.3

# Credits


Most stuff for this implementation were provided by and used from:


- [https://www.reddit.com/r/gamedev/comments/jumvi5/dualsense_haptics_leds_and_more_hid_output_report/](https://www.reddit.com/r/gamedev/comments/jumvi5/dualsense_haptics_leds_and_more_hid_output_report/)
- [https://github.com/Ryochan7/DS4Windows](https://github.com/Ryochan7/DS4Windows)

# Coming soon

- add multiple controllers
- add documentation using sphinx
