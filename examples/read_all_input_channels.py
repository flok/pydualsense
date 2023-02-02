import curses
import time
from pydualsense import *


dualsense = pydualsense()
dualsense.init()


while dualsense.states is None:
    print("no states found yet")
    print(f"epoch: {time.time():.0f}")
    time.sleep(0.5)


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()


while True:
    stdscr.addstr(0,  0, f"epoch: {time.time():.2f}")

    pretty_states = [f"{state:03}" for state in dualsense.states]

    stdscr.addstr(1, 0, f"states[0:10]:  {pretty_states[0:10]}")
    stdscr.addstr(2, 0, f"states[10:20]: {pretty_states[10:20]}")
    stdscr.addstr(3, 0, f"states[20:30]: {pretty_states[20:30]}")
    stdscr.addstr(4, 0, f"states[30:40]: {pretty_states[30:40]}")
    stdscr.addstr(5, 0, f"states[40:50]: {pretty_states[40:50]}")
    stdscr.addstr(6, 0, f"states[50:60]: {pretty_states[50:60]}")
    stdscr.addstr(7, 0, f"states[60:70]: {pretty_states[60:70]}")
    stdscr.addstr(8, 0, f"states[70:78]: {pretty_states[70:78]}")

    stdscr.addstr(11,  0, f"square: {dualsense.state.square} \t triangle: {dualsense.state.triangle} \t circle: {dualsense.state.circle} \t cross: {dualsense.state.cross}")
    stdscr.addstr(12,  0, f"DpadUp: {dualsense.state.DpadUp} \t DpadDown: {dualsense.state.DpadDown} \t DpadLeft: {dualsense.state.DpadLeft} \t DpadRight: {dualsense.state.DpadRight}")
    stdscr.addstr(13,  0, f"L1: {dualsense.state.L1} \t L2: {dualsense.state.L2} \t L3: {dualsense.state.L3} \t R1: {dualsense.state.R1} \t R2: {dualsense.state.R2} \t R3: {dualsense.state.R3} \t R2Btn: {dualsense.state.R2Btn} \t L2Btn: {dualsense.state.L2Btn}")
    stdscr.addstr(14,  0, f"share: {dualsense.state.share} \t options: {dualsense.state.options} \t ps: {dualsense.state.ps} \t touch1: {dualsense.state.touch1} \t touch2: {dualsense.state.touch2} \t touchBtn: {dualsense.state.touchBtn} \t touchRight: {dualsense.state.touchRight} \t touchLeft: {dualsense.state.touchLeft}")
    stdscr.addstr(15,  0, f"touchFinger1: {dualsense.state.touchFinger1} \t touchFinger2: {dualsense.state.touchFinger2}")
    stdscr.addstr(16,  0, f"micBtn: {dualsense.state.micBtn}")
    stdscr.addstr(17,  0, f"RX: {dualsense.state.RX} \t RY: {dualsense.state.RY} \t LX: {dualsense.state.LX} \t LY: {dualsense.state.LY}")
    stdscr.addstr(18,  0, f"trackPadTouch0: ID: {dualsense.state.trackPadTouch0.ID} \t isActive: {dualsense.state.trackPadTouch0.isActive} \t X: {dualsense.state.trackPadTouch0.X} \t Y: {dualsense.state.trackPadTouch0.Y}")
    stdscr.addstr(19,  0, f"trackPadTouch1: ID: {dualsense.state.trackPadTouch1.ID} \t isActive: {dualsense.state.trackPadTouch1.isActive} \t X: {dualsense.state.trackPadTouch1.X} \t Y: {dualsense.state.trackPadTouch1.Y}")
    stdscr.addstr(20, 0, f"gyro: roll: {dualsense.state.gyro.Roll} \t pitch: {dualsense.state.gyro.Pitch} \t yaw: {dualsense.state.gyro.Yaw}")
    stdscr.addstr(21, 0, f"acc: X: {dualsense.state.accelerometer.X} \t Y: {dualsense.state.accelerometer.Y} \t Z: {dualsense.state.accelerometer.Z}")

    stdscr.refresh()
    # time.sleep(0.1)

dualsense.close()

curses.echo()
curses.nobreak()
cursed.endwin()
