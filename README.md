# pydualsense
control your dualsense through python. using the hid library this module implements the sending report for controlling you new PS5 controller. It creates a background thread to constantly update the controller.

# dependecies

- hid >= 1.0.4

# usage

```python

from pydualsense import pydualsense

ds = pydualsense() # open controller
ds.setColor(255,0,0) # set touchpad color to red
ds.close() # closing the controller
```

# Coming soon

- reading the states of the controller to enable a fully compatibility with python
- add documentation