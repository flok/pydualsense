import argparse
from typing import Callable, Dict, Optional, Tuple

from .effects import main as run_effects
from .leds import main as run_leds
from .read_all_input_channels import main as run_read_input_channels
from .read_controller import main as run_read_controller
from .read_trigger_values import main as run_read_trigger_values

Example = Tuple[str, Callable[[], None]]
EXAMPLES: Dict[str, Example] = {
    "effects": ("Apply trigger and rumble effects. Press R1 to exit.", run_effects),
    "leds": ("Change the controller light and microphone mute setting.", run_leds),
    "read-controller": ("Print button, stick, and sensor events. Press R1 to exit.", run_read_controller),
    "read-input-channels": ("Print raw input values. Press Ctrl+C to exit.", run_read_input_channels),
    "read-trigger-values": ("Display L2 and R2 values for 30 seconds.", run_read_trigger_values),
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Browse and run pydualsense controller examples.",
        epilog="Run an example with: python -m pydualsense.examples EXAMPLE",
    )
    subparsers = parser.add_subparsers(dest="example", metavar="EXAMPLE")
    for name, (description, example_runner) in EXAMPLES.items():
        subparser = subparsers.add_parser(name, help=description)
        subparser.set_defaults(run_example=example_runner)

    args = parser.parse_args()

    run_example: Optional[Callable[[], None]] = getattr(args, "run_example", None)
    if run_example is None:
        parser.print_help()
        return

    run_example()


if __name__ == "__main__":
    main()
