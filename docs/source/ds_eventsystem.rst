pydualsense event system classes
================================

The `Event System` implements the event system used for the button callbacks

Controller callbacks run on one background thread in registration order, so a slow callback does not stop controller polling. Callback exceptions are logged and do not stop other callbacks. If callbacks fall behind, the bounded queue drops new event calls and logs a warning.

.. automodule:: pydualsense.event_system
   :noindex:
   :members:
   :undoc-members:
   :show-inheritance:
