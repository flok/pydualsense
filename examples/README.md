# Examples

Install pydualsense, connect the controller, and list available examples from any directory:

```console
python -m pip install pydualsense
python -m pydualsense.examples --help
```

Run an example by name:

```console
python -m pydualsense.examples read-controller
```

You can also run each module directly, such as `python -m pydualsense.examples.read_controller`.

The scripts in this folder are shortcuts for running the installed examples from a source checkout. The installed implementations live in `pydualsense.examples`.
