Usage
=====

Installation
------------

To use **pydualsense**, first install it using pip:

.. code-block:: console

   (.venv) $ pip install --upgrade pydualsense

This install the needed dependencies and the **pydualsense** library itself.


Windows
-------

The Windows HIDAPI DLL is included with the **pydualsense** package.


Linux based
-----------

On Linux, install HIDAPI through your package manager, then install pydualsense and its udev rule.

On Ubuntu systems the package `libhidapi-dev` is required.

.. code-block:: console

    sudo apt install libhidapi-dev

.. code-block:: console

    pip install --upgrade pydualsense
    sudo cp "$(python -c 'import pydualsense; print(pydualsense.__path__[0] + \"/70-ps5-controller.rules\")')" /etc/udev/rules.d/70-ps5-controller.rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger


Examples
--------

For code examles on using the library see :doc:`examples`
