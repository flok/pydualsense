from __future__ import annotations

import abc
import enum
import os
import sys
import hidapi
import threading

if sys.platform.startswith('Windows') and sys.version_info >= (3, 8):
    os.add_dll_directory(os.getcwd())

from .enums import LedOptions, PlayerID, PulseOptions, TriggerModeFlag, Brightness, ConnectionType


class HIDGuardianError(Exception):
    """
    The controller is protected by HIDGuardian.
    """


class DualSense:
    """
    A single DualSense controller.
    """

    @classmethod
    def find(cls) -> list[DualSense]:
        """
        Find connected DualSense controllers.

        :returns: The found device.
        :raises HIDGuardianError: If HIDGuardian is enabled.
        """

        # TODO: detect connection _mode, bluetooth has a bigger write buffer

        if sys.platform.startswith('win32'):
            import pydualsense.hidguardian as hidguardian
            if hidguardian.check_hide():
                raise HIDGuardianError('HIDGuardian detected. Delete the controller from HIDGuardian and restart PC to connect to controller')

        return list(
            map(
                lambda d: cls(device=d),
                map(
                    lambda d: hidapi.Device(vendor_id=d.vendor_id, product_id=d.product_id),
                    filter(
                        lambda d: d.vendor_id == 0x054c and d.product_id == 0x0CE6,
                        hidapi.enumerate(vendor_id=0x054c)
                    )
                )
            )
        )

    def __init__(self, device: hidapi.Device, microphone: Microphone = None):
        self.device: hidapi.Device = device
        """
        The :class:`~hidapi.Device` represented by this :class:`DualSense` object.
        """

        self.microphone: Microphone = microphone or Microphone()
        """
        The microphone of the controller.
        """

        self.cross: Button = Button()
        self.circle: Button = Button()
        self.triangle: Button = Button()
        self.square: Button = Button()

        self.left_stick: Stick = Stick()
        self.l1: Button = Button()
        self.l2: Trigger = Trigger()

        self.right_stick: Stick = Stick()
        self.r1: Button = Button()
        self.r2: Trigger = Trigger()

        self.share: Button = Button()
        self.options: Button = Button()
        self.ps: Button = Button()

        self.trackpad: Trackpad = Trackpad()

        self.player_id: PlayerID = PlayerID.OFF

    @property
    def l3(self) -> bool:
        return self.left_stick.pressed

    @property
    def r3(self) -> bool:
        return self.right_stick.pressed

    def init(self):
        """initialize module and device states
        """
        self.light = Light()  # control led light of ds
        self.audio = DSAudio()  # ds audio setting

        self.state = DSState()  # controller states

        if platform.startswith('Windows'):
            self.conType = self.determineConnectionType()  # determine USB or BT connection
        else:
            # set for usb manually
            self.input_report_length = 64
            self.output_report_length = 64

        # thread for receiving and sending
        self.ds_thread = True
        self.report_thread = threading.Thread(target=self.sendReport)
        self.report_thread.start()

    def determineConnectionType(self) -> ConnectionType:

        if self.device._device.input_report_length == 64:
            self.input_report_length = 64
            self.output_report_length = 64
            return ConnectionType.USB
        elif self.device._device.input_report_length == 78:
            self.input_report_length = 78
            self.output_report_length = 78
            return ConnectionType.BT

    def close(self):
        """
        Stops the report thread and closes the HID device
        """
        self.ds_thread = False
        self.report_thread.join()
        self.device.close()

    def setLeftMotor(self, intensity: int):
        """
        set left motor rumble

        Args:
            intensity (int): rumble intensity

        Raises:
            TypeError: intensity false type
            Exception: intensity out of bounds 0..255
        """
        if not isinstance(intensity, int):
            raise TypeError('left motor intensity needs to be an int')

        if intensity > 255 or intensity < 0:
            raise Exception('maximum intensity is 255')
        self.leftMotor = intensity

    def setRightMotor(self, intensity: int):
        """
        set right motor rumble

        Args:
            intensity (int): rumble intensity

        Raises:
            TypeError: intensity false type
            Exception: intensity out of bounds 0..255
        """
        if not isinstance(intensity, int):
            raise TypeError('right motor intensity needs to be an int')

        if intensity > 255 or intensity < 0:
            raise Exception('maximum intensity is 255')
        self.rightMotor = intensity

    def sendReport(self):
        """background thread handling the reading of the device and updating its states
        """
        while self.ds_thread:
            # read data from the input report of the controller
            inReport = self.device.read(self.input_report_length)
            if self.verbose:
                print(inReport)
            # decrypt the packet and bind the inputs
            self.readInput(inReport)

            # prepare new report for device
            outReport = self.prepareReport()

            # write the report to the device
            self.writeReport(outReport)

    def readInput(self, inReport):
        """
        read the input from the controller and assign the states

        Args:
            inReport (bytearray): read bytearray containing the state of the whole controller
        """
        states = list(inReport)  # convert bytes to list
        # states 0 is always 1
        self.state.LX = states[1] - 127
        self.state.LY = states[2] - 127
        self.state.RX = states[3] - 127
        self.state.RY = states[4] - 127
        self.state.L2 = states[5]
        self.state.R2 = states[6]

        # state 7 always increments -> not used anywhere

        buttonState = states[8]
        self.state.triangle = (buttonState & (1 << 7)) != 0
        self.state.circle = (buttonState & (1 << 6)) != 0
        self.state.cross = (buttonState & (1 << 5)) != 0
        self.state.square = (buttonState & (1 << 4)) != 0

        # dpad
        dpad_state = buttonState & 0x0F
        self.state.setDPadState(dpad_state)

        misc = states[9]
        self.state.R3 = (misc & (1 << 7)) != 0
        self.state.L3 = (misc & (1 << 6)) != 0
        self.state.options = (misc & (1 << 5)) != 0
        self.state.share = (misc & (1 << 4)) != 0
        self.state.R2Btn = (misc & (1 << 3)) != 0
        self.state.L2Btn = (misc & (1 << 2)) != 0
        self.state.R1 = (misc & (1 << 1)) != 0
        self.state.L1 = (misc & (1 << 0)) != 0

        misc2 = states[10]
        self.state.ps = (misc2 & (1 << 0)) != 0
        self.state.touchBtn = (misc2 & 0x02) != 0
        self.state.micBtn = (misc2 & 0x04) != 0

        # trackpad touch
        self.state.trackPadTouch0.ID = inReport[33] & 0x7F
        self.state.trackPadTouch0.isActive = (inReport[33] & 0x80) == 0
        self.state.trackPadTouch0.X = ((inReport[35] & 0x0f) << 8) | (inReport[34])
        self.state.trackPadTouch0.Y = ((inReport[36]) << 4) | ((inReport[35] & 0xf0) >> 4)

        # trackpad touch
        self.state.trackPadTouch1.ID = inReport[37] & 0x7F
        self.state.trackPadTouch1.isActive = (inReport[37] & 0x80) == 0
        self.state.trackPadTouch1.X = ((inReport[39] & 0x0f) << 8) | (inReport[38])
        self.state.trackPadTouch1.Y = ((inReport[40]) << 4) | ((inReport[39] & 0xf0) >> 4)

    # print(f'1Active = {self.state.trackPadTouch0.isActive}')
    # print(f'X1: {self.state.trackPadTouch0.X} Y2: {self.state.trackPadTouch0.Y}')

    # print(f'2Active = {self.state.trackPadTouch1.isActive}')
    # print(f'X2: {self.state.trackPadTouch1.X} Y2: {self.state.trackPadTouch1.Y}')
    # print(f'DPAD {self.state.DpadLeft} {self.state.DpadUp} {self.state.DpadRight} {self.state.DpadDown}')

    # TODO: implement gyrometer and accelerometer
    # TODO: control mouse with touchpad for fun as DS4Windows

    def writeReport(self, outReport):
        """
        write the report to the device

        Args:
            outReport (list): report to be written to device
        """
        self.device.write(bytes(outReport))

    def prepareReport(self):
        """
        prepare the output to be send to the controller

        Returns:
            list: report to send to controller
        """

        outReport = [0] * self.output_report_length  # create empty list with range of output report
        # packet type
        outReport[0] = 0x2

        # flags determing what changes this packet will perform
        # 0x01 set the main motors (also requires flag 0x02); setting this by itself will allow rumble to gracefully terminate and then re-enable audio haptics, whereas not setting it will kill the rumble instantly and re-enable audio haptics.
        # 0x02 set the main motors (also requires flag 0x01; without bit 0x01 motors are allowed to time out without re-enabling audio haptics)
        # 0x04 set the right trigger motor
        # 0x08 set the left trigger motor
        # 0x10 modification of audio volume
        # 0x20 toggling of internal speaker while headset is connected
        # 0x40 modification of microphone volume
        outReport[1] = 0xff  # [1]

        # further flags determining what changes this packet will perform
        # 0x01 toggling microphone LED
        # 0x02 toggling audio/mic mute
        # 0x04 toggling LED strips on the sides of the touchpad
        # 0x08 will actively turn all LEDs off? Convenience flag? (if so, third parties might not support it properly)
        # 0x10 toggling white player indicator LEDs below touchpad
        # 0x20 ???
        # 0x40 adjustment of overall motor/effect power (index 37 - read note on triggers)
        # 0x80 ???
        outReport[2] = 0x1 | 0x2 | 0x4 | 0x10 | 0x40  # [2]

        outReport[3] = self.leftMotor  # left low freq motor 0-255 # [3]
        outReport[4] = self.rightMotor  # right low freq motor 0-255 # [4]

        # outReport[5] - outReport[8] audio related

        # set Micrphone LED, setting doesnt effect microphone settings
        outReport[9] = self.audio.microphone_led  # [9]

        outReport[10] = 0x10 if self.audio.microphone_mute == True else 0x00

        # add right trigger _mode + parameters to packet
        outReport[11] = self.triggerR._mode.value
        outReport[12] = self.triggerR.forces[0]
        outReport[13] = self.triggerR.forces[1]
        outReport[14] = self.triggerR.forces[2]
        outReport[15] = self.triggerR.forces[3]
        outReport[16] = self.triggerR.forces[4]
        outReport[17] = self.triggerR.forces[5]
        outReport[20] = self.triggerR.forces[6]

        outReport[22] = self.triggerL._mode.value
        outReport[23] = self.triggerL.forces[0]
        outReport[24] = self.triggerL.forces[1]
        outReport[25] = self.triggerL.forces[2]
        outReport[26] = self.triggerL.forces[3]
        outReport[27] = self.triggerL.forces[4]
        outReport[28] = self.triggerL.forces[5]
        outReport[31] = self.triggerL.forces[6]

        outReport[39] = self.light.ledOption.value
        outReport[42] = self.light.pulseOptions.value
        outReport[43] = self.light.brightness.value
        outReport[44] = self.light.playerNumber.value
        outReport[45] = self.light.TouchpadColor[0]
        outReport[46] = self.light.TouchpadColor[1]
        outReport[47] = self.light.TouchpadColor[2]
        if self.verbose:
            print(outReport)
        return outReport


class DSTouchpad:
    def __init__(self) -> None:
        """
        Class represents the Trackpad of the controller
        """
        self.isActive = False
        self.ID = 0
        self.X = 0
        self.Y = 0


class DSState:

    def __init__(self) -> None:
        self.packerC = 0
        self.square, self.triangle, self.circle, self.cross = False, False, False, False
        self.DpadUp, self.DpadDown, self.DpadLeft, self.DpadRight = False, False, False, False
        self.L1, self.L2, self.L3, self.R1, self.R2, self.R3, self.R2Btn, self.L2Btn = False, False, False, False, False, False, False, False
        self.share, self.options, self.ps, self.touch1, self.touch2, self.touchBtn, self.touchRight, self.touchLeft = False, False, False, False, False, False, False, False
        self.touchFinger1, self.touchFinger2 = False, False
        self.RX, self.RY, self.LX, self.LY = 128, 128, 128, 128
        self.trackPadTouch0, self.trackPadTouch1 = DSTouchpad(), DSTouchpad()

    def setDPadState(self, dpad_state):



class Light:
    """
    The light features of the controller.
    """

    def __init__(self) -> None:
        self.brightness: Brightness = Brightness.low
        self.playerNumber: PlayerID = PlayerID.PLAYER_1
        self.ledOption: LedOptions = LedOptions.Both
        self.pulseOptions: PulseOptions = PulseOptions.Off
        self.TouchpadColor = (0, 0, 255)

    def setLEDOption(self, option: LedOptions):
        """
        Sets the LED Option

        Args:
            option (LedOptions): Led option

        Raises:
            TypeError: LedOption is false type
        """
        if not isinstance(option, LedOptions):
            raise TypeError('Need LEDOption type')
        self.ledOption = option

    def setPulseOption(self, option: PulseOptions):
        """
        Sets the Pulse Option of the LEDs

        Args:
            option (PulseOptions): pulse option of the LEDs

        Raises:
            TypeError: Pulse option is false type
        """
        if not isinstance(option, PulseOptions):
            raise TypeError('Need PulseOption type')
        self.pulseOptions = option

    def setBrightness(self, brightness: Brightness):
        """
        Defines the brightness of the Player LEDs

        Args:
            brightness (Brightness): brightness of LEDS

        Raises:
            TypeError: brightness false type
        """
        if not isinstance(brightness, Brightness):
            raise TypeError('Need Brightness type')
        self.brightness = brightness

    def setPlayerID(self, player: PlayerID):
        """
        Sets the PlayerID of the controller with the choosen LEDs.
        The controller has 4 Player states

        Args:
            player (PlayerID): chosen PlayerID for the Controller

        Raises:
            TypeError: [description]
        """
        if not isinstance(player, PlayerID):
            raise TypeError('Need PlayerID type')
        self.playerNumber = player

    def setColorI(self, r: int, g: int, b: int) -> None:
        """
        Sets the Color around the Trackpad of the controller

        Args:
            r (int): red channel
            g (int): green channel
            b (int): blue channel

        Raises:
            TypeError: color channels have wrong type
            Exception: color channels are out of bounds
        """
        if not isinstance(r, int) or not isinstance(g, int) or not isinstance(b, int):
            raise TypeError('Color parameter need to be int')
        # check if color is out of bounds
        if (r > 255 or g > 255 or b > 255) or (r < 0 or g < 0 or b < 0):
            raise Exception('colors have values from 0 to 255 only')
        self.TouchpadColor = (r, g, b)

    def setColorT(self, color: tuple) -> None:
        """
        Sets the Color around the Trackpad as a tuple

        Args:
            color (tuple): color as tuple

        Raises:
            TypeError: color has wrong type
            Exception: color channels are out of bounds
        """
        if not isinstance(color, tuple):
            raise TypeError('Color type is tuple')
        # unpack for out of bounds check
        r, g, b = map(int, color)
        # check if color is out of bounds
        if (r > 255 or g > 255 or b > 255) or (r < 0 or g < 0 or b < 0):
            raise Exception('colors have values from 0 to 255 only')
        self.TouchpadColor = (r, g, b)


class Button:
    """
    A button of the :class:`.DualSense`.
    """

    def __init__(self):
        self.pressed: bool = False

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {'_' if self.pressed else '-'}>"


class TrackpadTouch:
    """
    .. todo:: Find out what each field means.
    """

    def __init__(self):
        self.id = 0
        self.active = False
        self.x = 0
        self.y = 0


class Trackpad(Button):
    """
    The trackpad of the :class:`.DualSense`, which also behaves as a button.
    """

    def __init__(self):
        super().__init__()
        self.touches: list[TrackpadTouch] = [TrackpadTouch(), TrackpadTouch()]

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {'_' if self.pressed else '-'} with {len(self.touches)} touches>"


class Microphone(Button):
    """
    The microphone peripheral of the :class:`.DualSense`, which also behaves as a button.
    """

    def __init__(self) -> None:
        super().__init__()

        self.enabled: bool = True
        """
        If the mic is capturing audio.
        """

        self.led_lit: bool = False
        """
        If the mic LED is switched on.
        """

    def __repr__(self):
        return f"<Microphone {'_' if self.pressed else '-'} {'enabled' if self.enabled else 'muted'} with LED {'on' if self.led_lit else 'off'}>"

    def mute(self):
        """
        Mute the mic and switch on the LED.
        """
        self.enabled = False
        self.led_lit = True

    def unmute(self):
        """
        Unmute the mic and switch off the LED.
        """
        self.enabled = True
        self.led_lit = False


class TriggerMode:
    """
    Generic class for representing any trigger mode.

    .. todo:: Extend this class with additional ones that allow tweaking the force values in a user-friendly way.
    """

    def __init__(self, flag: TriggerModeFlag, forces: list[int] = None):
        self.flag: TriggerModeFlag = flag
        self.forces: list[int] = forces or [0] * 8

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.flag!r}: {self.forces!r}>"


class Trigger(Button):
    """
    One of the two triggers of the :class:`.DualSense`, which additionally behaves as a digital button.
    """

    def __init__(self) -> None:
        super().__init__()

        self.mode: TriggerMode = TriggerMode(TriggerModeFlag.OFF)
        """
        The feedback mode of the trigger.
        
        .. seealso:: :class:`.TriggerModes`
        """

        self.position: int = 0
        """
        The position the trigger is currently in.
        """

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.position}{'_' if self.pressed else '-'} {self.position} {self.mode}>"


class Stick(Button):
    """
    One of the two sticks of the :class:`.DualSense`.
    """

    def __init__(self):
        super().__init__()
        
        self.x: int = 0
        """
        The horizontal position of the stick, from -127 to 127.
        """

        self.y: int = 0
        """
        The vertical position of the stick, from -127 to 127.
        """

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {'_' if self.pressed else '-'} at {self.x}, {self.y}>"


class DPad:
    """
    The DPad of the :class:`.DualSense`.
    """

    def __init__(self):
        self.up: bool = False
        self.down: bool = False
        self.right: bool = False
        self.left: bool = False

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {'↑' if self.up else ''}{'→' if self.right else ''}{'↓' if self.down else ''}{'←' if self.left else ''}>"

    @property
    def state(self):
        return {
            ( True, False, False, False): 0,
            ( True, False, False,  True): 1,
            (False, False, False,  True): 2,
            (False,  True, False,  True): 3,
            (False,  True, False, False): 4,
            (False,  True,  True, False): 5,
            (False, False,  True, False): 6,
            (True,  False,  True, False): 7,
        }[self.up, self.down, self.left, self.right]
    
    @state.setter
    def state(self, value):
        self.up = value == 0 or value == 1 or value == 7
        self.down = value == 3 or value == 4 or value == 5
        self.left = value == 5 or value == 6 or value == 7
        self.right = value == 1 or value == 2 or value == 3
