import hid
from enums import (LedOptions, PlayerID,
                   PulseOptions, TriggerModes, Brightness)
import threading

class pydualsense:

    def __init__(self) -> None:
        # TODO: maybe add a init function to not automatically allocate controller when class is declared
        self.device = self.__find_device()
        self.light = DSLight() # control led light of ds
        self.audio = DSAudio()
        self.triggerL = DSTrigger()
        self.triggerR = DSTrigger()

        # set default for the controller
        self.color = (0,0,255) # set dualsense color around the touchpad to blue

        self.send_thread = True
        send_report = threading.Thread(target=self.sendReport)
        #send_report.start()
        # create thread for sending

    def __find_device(self):
        devices = hid.enumerate(vid=0x054c)
        found_devices = []
        for device in devices:
            if device['vendor_id'] == 0x54c and device['product_id'] == 0xCE6:
                found_devices.append(device)

        # TODO: detect connection mode, bluetooth has a bigger write buffer
        # TODO: implement multiple controllers working
        if len(found_devices) != 1:
            raise Exception('no dualsense controller detected')

   
        dual_sense = hid.Device(vid=found_devices[0]['vendor_id'], pid=found_devices[0]['product_id'])
        return dual_sense
    

    # color stuff
    def setColor(self, r: int, g:int, b:int):
        if r > 255 or g > 255 or b > 255:
            raise Exception('colors have values from 0 to 255 only')
        self.color = (r,g,b)


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
        self.audio.microphoneLED = 0x1


    def sendReport(self):
       # while self.send_thread:
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
        
        outReport[3]= 0 # left low freq motor 0-255 # [3]
        outReport[4] = 0 # right low freq motor 0-255 # [4]


        # outReport[5] - outReport[8] audio related
        

        # set Micrphone LED, setting doesnt effect microphone settings
        outReport[9] = self.audio.microphone_led # [9]

        # set microphone muting
        


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


        """
        outReport.append(self.light.ledOption.value[0]) # 
        outReport.append(self.light.pulseOptions.value[0])
        outReport.append(self.light.brightness.value[0])
        outReport.append(self.light.playerNumber.value[0])
        outReport.append(self.color[0]) # r
        outReport.append(self.color[1]) # g
        outReport.append(self.color[2]) # b
        """
        outReport[39] = self.light.ledOption.value
        outReport[42] = self.light.pulseOptions.value
        outReport[43] = self.light.brightness.value
        outReport[44] = self.light.playerNumber.value
        outReport[45] = self.color[0]
        outReport[46] = self.color[1]
        outReport[47] = self.color[2]
        self.device.write(bytes(outReport)) # send to controller



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
    
if __name__ == "__main__":
    ds = pydualsense()
    import time
  #  ds.triggerR.setMode(TriggerModes.Rigid)
 #   ds.triggerR.setForce(0, 255)
    ds.setLeftTriggerMode(TriggerModes.Pulse)
    ds.setLeftTriggerForce(1, 255)
    ds.setRightTriggerMode(TriggerModes.Rigid)
    ds.setRightTriggerForce(1, 255)
#    ds.triggerL.setForce(6,255)
    ds.sendReport()
    time.sleep(2)
    time.sleep(3)