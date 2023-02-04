import curses
import time
from pydualsense import *


def print_states(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    stdscr.nodelay(1)
    while True:
        stdscr.erase()
        pretty_states = [f"{state:03}" for state in dualsense.states]

        stdscr.addstr(f"epoch: {time.time():.2f}\n")
        stdscr.addstr(f"states[0:10]:  {pretty_states[0:10]}\n")
        stdscr.addstr(f"states[10:20]: {pretty_states[10:20]}\n")
        stdscr.addstr(f"states[20:30]: {pretty_states[20:30]}\n")
        stdscr.addstr(f"states[30:40]: {pretty_states[30:40]}\n")
        stdscr.addstr(f"states[40:50]: {pretty_states[40:50]}\n")
        stdscr.addstr(f"states[50:60]: {pretty_states[50:60]}\n")
        stdscr.addstr(f"states[60:70]: {pretty_states[60:70]}\n")
        stdscr.addstr(f"states[70:78]: {pretty_states[70:78]}\n")
        stdscr.addstr("\n")
        stdscr.addstr(f"square: {dualsense.state.square!s:>5} \t triangle: {dualsense.state.triangle!s:>5} \t circle: {dualsense.state.circle!s:>5} \t cross: {dualsense.state.cross!s:>5}\n")
        stdscr.addstr(f"DpadUp: {dualsense.state.DpadUp!s:>5} \t DpadDown: {dualsense.state.DpadDown!s:>5} \t DpadLeft: {dualsense.state.DpadLeft!s:>5} \t DpadRight: {dualsense.state.DpadRight!s:>5}\n")
        stdscr.addstr(f"L1: {dualsense.state.L1!s:>5} \t L2: {dualsense.state.L2:3} \t L2Btn: {dualsense.state.L2Btn!s:>5} \t L3: {dualsense.state.L3!s:>5} \t R1: {dualsense.state.R1!s:>5} \t R2: {dualsense.state.R2:3d} \t R2Btn: {dualsense.state.R2Btn!s:>5} \t R3: {dualsense.state.R3!s:>5}\n")
        stdscr.addstr(f"share: {dualsense.state.share!s:>5} \t options: {dualsense.state.options!s:>5} \t ps: {dualsense.state.ps!s:>5} \t touch1: {dualsense.state.touch1!s:>5} \t touch2: {dualsense.state.touch2!s:>5} \t touchBtn: {dualsense.state.touchBtn!s:>5} \t touchRight: {dualsense.state.touchRight!s:>5} \t touchLeft: {dualsense.state.touchLeft!s:>5}\n")
        stdscr.addstr(f"touchFinger1: {dualsense.state.touchFinger1} \t touchFinger2: {dualsense.state.touchFinger2}\n")
        stdscr.addstr(f"micBtn: {dualsense.state.micBtn!s:>5}\n")
        stdscr.addstr(f"RX: {dualsense.state.RX:4} \t RY: {dualsense.state.RY:4} \t LX: {dualsense.state.LX:4} \t LY: {dualsense.state.LY:4}\n")
        stdscr.addstr(f"trackPadTouch0: ID: {dualsense.state.trackPadTouch0.ID} \t isActive: {dualsense.state.trackPadTouch0.isActive!s:>5} \t X: {dualsense.state.trackPadTouch0.X:4d} \t Y: {dualsense.state.trackPadTouch0.Y:4d}\n")
        stdscr.addstr(f"trackPadTouch1: ID: {dualsense.state.trackPadTouch1.ID} \t isActive: {dualsense.state.trackPadTouch1.isActive!s:>5} \t X: {dualsense.state.trackPadTouch1.X:4d} \t Y: {dualsense.state.trackPadTouch1.Y:4d}\n")
        stdscr.addstr(f"gyro: roll: {dualsense.state.gyro.Roll:6} \t pitch: {dualsense.state.gyro.Pitch:6} \t yaw: {dualsense.state.gyro.Yaw:6}\n")
        stdscr.addstr(f"acc: X: {dualsense.state.accelerometer.X:6} \t Y: {dualsense.state.accelerometer.Y:6} \t Z: {dualsense.state.accelerometer.Z:6}\n")
        stdscr.addstr("\n")
        stdscr.addstr("Exit script with 'q'\n")

        stdscr.refresh()
        if stdscr.getch() == ord('q'):
            break


dualsense = pydualsense()
dualsense.init()

while dualsense.states is None:
    print("Waiting until connection is established...")
    print(f"epoch: {time.time():.0f}")
    time.sleep(0.5)


curses.wrapper(print_states)
dualsense.close()
