from os import device_encoding
import hid # type: ignore
from .enums import (LedOptions, PlayerID,
                   PulseOptions, TriggerModes, Brightness)
import threading
import sys
import winreg
class pydualsense:

    def __init__(self, verbose: bool = False) -> None:#
        # TODO: maybe add a init function to not automatically allocate controller when class is declared
        self.verbose = verbose
        self.receive_buffer_size = 64
        self.send_report_size = 48

        self.leftMotor = 0
        self.rightMotor = 0


    def init(self):
        """initialize module and device states
        """
        self.device: hid.Device = self.__find_device()
        self.light = DSLight() # control led light of ds
        self.audio = DSAudio() # ds audio setting
        self.triggerL = DSTrigger() # left trigger
        self.triggerR = DSTrigger() # right trigger

        self.state = DSState() # controller states


        # thread for receiving and sending
        self.ds_thread = True
        self.report_thread = threading.Thread(target=self.sendReport)
        self.report_thread.start()

        self.init = True

    def close(self):
        """
        Stops the report thread and closes the HID device
        """
        self.ds_thread = False
        self.report_thread.join()
        self.device.close()

    def _check_hide(self) -> bool:
        """check if hidguardian is used and controller is hidden
        """
        if sys.platform.startswith('win32'):
            try:
                access_reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
                access_key = winreg.OpenKey(access_reg, 'SYSTEM\CurrentControlSet\Services\HidGuardian\Parameters', 0, winreg.KEY_READ)
                affected_devices = winreg.QueryValueEx(access_key, 'AffectedDevices')[0]
                if "054C" in affected_devices and "0CE6" in affected_devices:
                    return True
                return False
            except OSError as e:
                print(e)

        return False


    def __find_device(self) -> hid.Device:
        """
        find HID device and open it

        Raises:
            Exception: HIDGuardian detected
            Exception: No device detected

        Returns:
            hid.Device: returns opened controller device
        """
        # TODO: detect connection mode, bluetooth has a bigger write buffer
        # TODO: implement multiple controllers working
        if self._check_hide():
            raise Exception('HIDGuardian detected. Delete the controller from HIDGuardian and restart PC to connect to controller')
        detected_device: hid.Device = None
        devices = hid.enumerate(vid=0x054c)
        for device in devices:
            if device['vendor_id'] == 0x054c and device['product_id'] == 0x0CE6:
                detected_device = device


        if detected_device == None:
            raise Exception('No device detected')

        dual_sense = hid.Device(vid=detected_device['vendor_id'], pid=detected_device['product_id'])
        return dual_sense

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
            inReport = self.device.read(self.receive_buffer_size)

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
        states = list(inReport) # convert bytes to list
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
        outReport = [0] * 48 # create empty list with range of output report
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
        outReport[1] = 0xff # [1]

        # further flags determining what changes this packet will perform
        # 0x01 toggling microphone LED
        # 0x02 toggling audio/mic mute
        # 0x04 toggling LED strips on the sides of the touchpad
        # 0x08 will actively turn all LEDs off? Convenience flag? (if so, third parties might not support it properly)
        # 0x10 toggling white player indicator LEDs below touchpad
        # 0x20 ???
        # 0x40 adjustment of overall motor/effect power (index 37 - read note on triggers)
        # 0x80 ???
        outReport[2] = 0x1 | 0x2 | 0x4 | 0x10 | 0x40 # [2]

        outReport[3] = self.leftMotor # left low freq motor 0-255 # [3]
        outReport[4] = self.rightMotor # right low freq motor 0-255 # [4]

        # outReport[5] - outReport[8] audio related

        # set Micrphone LED, setting doesnt effect microphone settings
        outReport[9] = self.audio.microphone_led # [9]

        # add right trigger mode + parameters to packet
        outReport[11] = self.triggerR.mode.value
        outReport[12] = self.triggerR.forces[0]
        outReport[13] = self.triggerR.forces[1]
        outReport[14] = self.triggerR.forces[2]
        outReport[15] = self.triggerR.forces[3]
        outReport[16] = self.triggerR.forces[4]
        outReport[17] = self.triggerR.forces[5]
        outReport[20] = self.triggerR.forces[6]

        outReport[22] = self.triggerL.mode.value
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
        Class represents the Touchpad of the controller
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
        self.RX, self.RY, self.LX, self.LY = 128,128,128,128
        self.trackPadTouch0, self.trackPadTouch1 = DSTouchpad(), DSTouchpad()

    def setDPadState(self, dpad_state):
        if dpad_state == 0:
            self.DpadUp = True
            self.DpadDown = False
            self.DpadLeft = False
            self.DpadRight = False
        elif dpad_state == 1:
            self.DpadUp = True
            self.DpadDown = False
            self.DpadLeft = False
            self.DpadRight = True
        elif dpad_state == 2:
            self.DpadUp = False
            self.DpadDown = False
            self.DpadLeft = False
            self.DpadRight = True
        elif dpad_state == 3:
            self.DpadUp = False
            self.DpadDown = True
            self.DpadLeft = False
            self.DpadRight = True
        elif dpad_state == 4:
            self.DpadUp = False
            self.DpadDown = True
            self.DpadLeft = False
            self.DpadRight = False
        elif dpad_state == 5:
            self.DpadUp = False
            self.DpadDown = True
            self.DpadLeft = False
            self.DpadRight = False
        elif dpad_state == 6:
            self.DpadUp = False
            self.DpadDown = False
            self.DpadLeft = True
            self.DpadRight = False
        elif dpad_state == 7:
            self.DpadUp = True
            self.DpadDown = False
            self.DpadLeft = True
            self.DpadRight = False
        else:
            self.DpadUp = False
            self.DpadDown = False
            self.DpadLeft = False
            self.DpadRight = False


class DSLight:
    """
    Represents all features of lights on the controller
    """
    def __init__(self) -> None:
        self.brightness: Brightness = Brightness.low # sets
        self.playerNumber: PlayerID = PlayerID.player1
        self.ledOption : LedOptions = LedOptions.Both
        self.pulseOptions : PulseOptions = PulseOptions.Off
        self.TouchpadColor = (0,0,255)

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

    def setPlayerID(self, player : PlayerID):
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

    def setColorI(self, r: int , g: int, b: int) -> None:
        """
        Sets the Color around the Touchpad of the controller

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
        self.TouchpadColor = (r,g,b)


    def setColorT(self, color: tuple) -> None:
        """
        Sets the Color around the Touchpad as a tuple

        Args:
            color (tuple): color as tuple

        Raises:
            TypeError: color has wrong type
            Exception: color channels are out of bounds
        """
        if not isinstance(color, tuple):
            raise TypeError('Color type is tuple')
        # unpack for out of bounds check
        r,g,b = map(int, color)
        # check if color is out of bounds
        if (r > 255 or g > 255 or b > 255) or (r < 0 or g < 0 or b < 0):
            raise Exception('colors have values from 0 to 255 only')
        self.TouchpadColor = (r,g,b)


class DSAudio:
    def __init__(self) -> None:
        self.microphone_mute = 0
        self.microphone_led = 0

    def setMicrophoneLED(self, value):
        """
        Activates or disables the microphone led.
        This doesnt change the mute/unmutes the microphone itself.

        Args:
            value (int): On or off microphone LED

        Raises:
            Exception: false state for the led
        """
        if value > 1 or value < 0:
            raise Exception('Microphone LED can only be on or off (0 .. 1)')
        self.microphone_led = value

class DSTrigger:
    def __init__(self) -> None:
        # trigger modes
        self.mode : TriggerModes = TriggerModes.Off

        # force parameters for the triggers
        self.forces = [0 for i in range(7)]

    def setForce(self, forceID: int = 0, force: int = 0):
        """
        Sets the forces of the choosen force parameter

        Args:
            forceID (int, optional): force parameter. Defaults to 0.
            force (int, optional): applied force to the parameter. Defaults to 0.

        Raises:
            TypeError: wrong type of forceID or force
            Exception: choosen a false force parameter
        """
        if not isinstance(forceID, int) or not isinstance(force, int):
            raise TypeError('forceID and force needs to be type int')

        if forceID > 6 or forceID < 0:
            raise Exception('only 7 parameters available')

        self.forces[forceID] = force

    def setMode(self, mode: TriggerModes):
        """
        Set the Mode for the Trigger

        Args:
            mode (TriggerModes): Trigger mode

        Raises:
            TypeError: false Trigger mode type
        """
        if not isinstance(mode, TriggerModes):
            raise TypeError('Trigger mode parameter needs to be of type `TriggerModes`')

        self.mode = mode