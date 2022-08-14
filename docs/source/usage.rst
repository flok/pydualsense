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

If you are on Windows the hidapi need to downloaded from `here <https://github.com/libusb/hidapi/releases>`_. 
The downloaded `.dll` file need to be placed in a path that is in your environments variable `path`.


Linux based
-----------

If you are on a linux based system (e.g debian) you need to first need to install the hidapi through your package manager.

On Ubuntu systems the package `libhidapi-dev` is required.

.. code-block:: console

    sudo apt install libhidapi-dev


Examples
--------

For code examles on using the library see :doc:`examples`