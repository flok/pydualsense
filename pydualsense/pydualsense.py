import hid
from .enums import (LedOptions, PlayerID,
                   PulseOptions, TriggerModes, Brightness)
import threading

class pydualsense:

    def __init__(self, verbose: bool = False) -> None:
        # TODO: maybe add a init function to not automatically allocate controller when class is declared
        self.verbose = verbose

        self.device: hid.Device = self.__find_device()



        self.light = DSLight() # control led light of ds
        self.audio = DSAudio()
        self.triggerL = DSTrigger()
        self.triggerR = DSTrigger()

        self.color = (0,0,255) # set color around touchpad to blue


        self.receive_buffer_size = 64
        self.send_report_size = 48
        # controller states
        self.state = DSState()

        # thread for receiving and sending
        self.ds_thread = True
        self.report_thread = threading.Thread(target=self.sendReport)
        self.report_thread.start()

    def close(self):
        self.ds_thread = False
        self.report_thread.join()
        self.device.close()

    def __find_device(self):
        devices = hid.enumerate(vid=0x054c)
        found_devices = []
        for device in devices:
            if device['vendor_id'] == 0x054c and device['product_id'] == 0x0CE6:
                found_devices.append(device)

        # TODO: detect connection mode, bluetooth has a bigger write buffer
        # TODO: implement multiple controllers working
        if len(found_devices) != 1:
            raise Exception('no dualsense controller detected')


        dual_sense = hid.Device(vid=found_devices[0]['vendor_id'], pid=found_devices[0]['product_id'])
        return dual_sense



    # right trigger
    def setRightTriggerMode(self, mode: TriggerModes):
        """set the trigger mode for R2

        :param mode: enum of Trigger mode
        :type mode: TriggerModes
        """
        self.triggerR.mode = mode

    def setRightTriggerForce(self, forceID: int, force: int):
        """set the right trigger force. trigger consist of 7 parameter

        :param forceID: parameter id from  0 to 6
        :type forceID: int
        :param force: force from 0..ff (0..255) applied to the trigger
        :type force: int
        """
        if forceID > 6:
            raise Exception('only 7 parameters available')

        self.triggerR.setForce(id=forceID, force=force)


    # left trigger
    def setLeftTriggerMode(self, mode: TriggerModes):
        """set the trigger mode for L2

        :param mode: enum of Trigger mode
        :type mode: TriggerModes
        """
        self.triggerL.mode = mode

    def setLeftTriggerForce(self, forceID: int, force: int):
        """set the left trigger force. trigger consist of 7 parameter

        :param forceID: parameter id from  0 to 6
        :type forceID: int
        :param force: force from 0..ff (0..255) applied to the trigger
        :type force: int
        """

        if forceID > 6:
            raise Exception('only 7 parameters available')
        self.triggerL.setForce(id=forceID, force=force)


    # TODO: audio
    # audio stuff
    def setMicrophoneLED(self, value):
        self.audio.microphone_led = value

    # color stuff
    def setColor(self, r: int, g:int, b:int):
        """sets the led colour around the touchpad

        :param r: red channel, 0..255
        :type r: int
        :param g: green channel, 0..255
        :type g: int
        :param b: blue channel, 0..255
        :type b: int
        :raises Exception: wron color values
        """
        if (r > 255 or g > 255 or b > 255) or (r < 0 or g < 0 or b < 0):
            raise Exception('colors have values from 0 to 255 only')
        self.color = (r,g,b)

    def setLEDOption(self, option: LedOptions):
        """set led option

        :param option: led option
        :type option: LedOptions
        """
        self.light.ledOption = option

    def setPulseOption(self, option: PulseOptions):
        """set the pulse option for the leds

        :param option: [description]
        :type option: PulseOptions
        """
        self.light.pulseOptions = option

    def setBrightness(self, brightness: Brightness):
        """set the brightness of the player leds

        :param brightness: brightness for the leds
        :type brightness: Brightness
        """
        self.light.brightness = brightness

    def setPlayerID(self, player : PlayerID):
        """set the player ID. The controller has 5 white LED which signals
        which player the controller is

        :param player: the player id from 1 to 5
        :type player: PlayerID
        """
        self.light.playerNumber = player

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
        """read the reported data from the controller

        :param inReport: report of the controller
        :type inReport: bytes
        """
        states = list(inReport) # convert bytes to list
        # states 0 is always 1
        self.state.LX = states[1]
        self.state.LY = states[2]
        self.state.RX = states[3]
        self.state.RY = states[4]
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
        """Write the given report to the device

        :param outReport: report with data for the controller
        :type outReport: list
        """
        self.device.write(bytes(outReport))


    def prepareReport(self):
        """prepare the report for the controller with all the settings set since the previous update

        :return: report for the controller with all infos
        :rtype: list
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

        outReport[3] = 0 # left low freq motor 0-255 # [3]
        outReport[4] = 0 # right low freq motor 0-255 # [4]

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
        outReport[45] = self.color[0]
        outReport[46] = self.color[1]
        outReport[47] = self.color[2]
        if self.verbose:
            print(outReport)
        return outReport

class DSTouchpad:
    def __init__(self) -> None:
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
    """DualSense Light class

        make it simple, no get or set functions. quick and dirty
    """
    def __init__(self) -> None:
        self.brightness: Brightness = Brightness.low # sets
        self.playerNumber: PlayerID = PlayerID.player1
        self.ledOption : LedOptions = LedOptions.Both
        self.pulseOptions : PulseOptions = PulseOptions.Off

    def setBrightness(self, brightness: Brightness):
        self._brightness = brightness

    def setPlayerNumer(self, player):
        if player > 5:
            raise Exception('only 5 players supported. choose 1-5')



class DSAudio:
    def __init__(self) -> None:
        self.microphone_mute = 0
        self.microphone_led = 0

class DSTrigger:
    def __init__(self) -> None:
        # trigger modes
        self.mode : TriggerModes = TriggerModes.Off

        # force parameters for the triggers
        self.forces = [0 for i in range(7)]

    def setForce(self, id:int = 0, force:int = 0):
        """set the force of the trigger

        :param id: id of the trigger parameters. 6 possible, defaults to 0
        :type id: int, optional
        :param force: force 0 to 255, defaults to 0
        :type force: int, optional
        :raises Exception: false trigger parameter accessed. only available trigger parameters from 0 to 6
        """
        if id > 6 or id < 0:
            raise Exception('only trigger parameters 0 to 6 available')
        self.forces[id] = force

    def setMode(self, mode: TriggerModes):
        """set mode on the trigger

        :param mode: mode for trigger
        :type mode: TriggerModes
        """
        self.mode = mode

    def getTriggerPacket(self):
        """returns array of the trigger modes and its parameters

        :return: packet of the trigger settings
        :rtype: list
        """
        # create packet
        packet = [self.mode.value]
        packet += [self.forces[i] for i in range(6)]
        packet += [0,0] # unknown what these do ?
        packet.append(self.forces[-1]) # last force has a offset of 2 from the other forces. this is the frequency of the actuation
        return packet
