# pydualsense
control your dualsense through python. using the hid library this module implements the sending report for controlling you new PS5 controller. It creates a background thread to constantly update the controller.

# install

Just install the package from pypi

```bash
pip install pydualsense
```
# usage

```python

from pydualsense import pydualsense

ds = pydualsense() # open controller
ds.setColor(255,0,0) # set touchpad color to red
ds.setLeftTriggerMode(TriggerModes.Rigid)
ds.setLeftTriggerForce(1, 255)
ds.close() # closing the controller
```
# dependecies

- hid >= 1.0.4
# Coming soon

- reading the states of the controller to enable a fully compatibility with python - partially done
- add documentation using sphinx