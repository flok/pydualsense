# pydualsense
control your dualsense through python. using the hid library this package implements the report features for controlling your PS5 controller.

# Documentation

You can find the documentation at [docs](https://flok.github.io/pydualsense/)

# Installation


## Windows

The Windows HIDAPI DLL is included with the package. Install pydualsense from [PyPI](https://pypi.org/project/pydualsense/):

```bash
pip install --upgrade pydualsense
```

## Linux

On Ubuntu, install HIDAPI and pydualsense, then install the udev rule so your user can access the controller without root privileges.

```bash
sudo apt install libhidapi-dev
pip install --upgrade pydualsense
sudo cp "$(python -c 'import pydualsense; print(pydualsense.__path__[0] + "/70-ps5-controller.rules")')" /etc/udev/rules.d/70-ps5-controller.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

# usage

```python

from pydualsense import pydualsense, TriggerModes

def cross_pressed(state):
    print(state)

with pydualsense() as ds:
    ds.cross_pressed += cross_pressed
    ds.light.setColorI(255, 0, 0) # set touchpad color to red
    ds.triggerL.setMode(TriggerModes.Rigid)
    ds.triggerL.setForce(1, 255)
```

List and run examples after installation with `python -m pydualsense.examples --help`. See the [examples guide](https://flok.github.io/pydualsense/examples.html) for details.

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
