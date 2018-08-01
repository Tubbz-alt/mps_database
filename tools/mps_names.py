from mps_config import MPSConfig, models

class MpsName:
    def __init__(self, session):
        self.session = session

    def getDeviceInputNameFromId(self, deviceInputId):
        deviceInput = self.session.query(models.DeviceInput).filter(models.DeviceInput.id==deviceInputId).one()
        return self.getDeviceInputName(deviceInput)

    def getDeviceInputBaseName(self, deviceInput):
        digitalChannel = self.session.query(models.DigitalChannel).filter(models.DigitalChannel.id==deviceInput.channel_id).one()
        device = self.session.query(models.DigitalDevice).filter(models.DigitalDevice.id==deviceInput.digital_device_id).one()
        if device.measured_device_type_id == None:
            deviceType = self.session.query(models.DeviceType).filter(models.DeviceType.id==device.device_type_id).one()
        else:
            deviceType = self.session.query(models.DeviceType).filter(models.DeviceType.id==device.measured_device_type_id).one()

        return deviceType.name + ":" + device.area + ":" + str(device.position)

    def getDeviceInputName(self, deviceInput):
        digitalChannel = self.session.query(models.DigitalChannel).filter(models.DigitalChannel.id==deviceInput.channel_id).one()
        device = self.session.query(models.DigitalDevice).filter(models.DigitalDevice.id==deviceInput.digital_device_id).one()
        if device.measured_device_type_id == None:
            deviceType = self.session.query(models.DeviceType).filter(models.DeviceType.id==device.device_type_id).one()
        else:
            deviceType = self.session.query(models.DeviceType).filter(models.DeviceType.id==device.measured_device_type_id).one()

        return deviceType.name + ":" + device.area + ":" + str(device.position) + ":" + digitalChannel.name

    def getAnalogDeviceNameFromId(self, analogDeviceId):
        analogDevice = self.session.query(models.AnalogDevice).filter(models.AnalogDevice.id==analogDeviceId).one()
        
        return self.getAnalogDeviceName(analogDevice)

    def getAnalogDeviceName(self, analogDevice):
        deviceType = self.session.query(models.DeviceType).filter(models.DeviceType.id==analogDevice.device_type_id).one()
        
        return deviceType.name + ":" + analogDevice.area + ":" + str(analogDevice.position)

    def getBeamDestinationNameFromId(self, beamDestinationId):
        beamDestination = self.session.query(models.BeamDestination).filter(models.BeamDestination.id==beamDestinationId).one()
        
        return self.getBeamDestinationName(beamDestination)

    def getBeamDestinationName(self, beamDestination):
        return "$(BASE):" + beamDestination.name.upper() + "_PC"

    def getFaultNameFromId(self, faultId):
        fault = self.session.query(models.Fault).filter(models.Fault.id==fauldId).one()

        return self.getFaultName(fault)

    def getFaultName(self, fault):
        is_digital = True

        if len(fault.inputs) <= 0:
            print 'ERROR: Fault {0} (id={1}) has no inputs, can\'t proceed. exiting...'.format(fault.name, fault.id)
            exit(1)

        for fault_input in fault.inputs:
            if fault_input.bit_position == 0:
                try:
                    device = self.session.query(models.DigitalDevice).filter(models.DigitalDevice.id==fault_input.device_id).one()
                    for input in device.inputs:
                        if input.bit_position == 0:
                            device_input = input
                except:
                    is_digital = False

                if not is_digital:
                    try:
                        device = self.session.query(models.AnalogDevice).filter(models.AnalogDevice.id==fault_input.device_id).one()
                    except:
                        print "Bonkers, device " + str(fault_input.device_id) + " is not digital nor analog - what?!?"
                        
        if is_digital:
            base = self.getDeviceInputBaseName(device_input)
        else:
            base = self.getAnalogDeviceName(device)

        return base + ":" + fault.name + "_FLT"

    def getConditionName(self, condition):
        return "$(BASE):" + condition.name.upper() + "_COND"

    #
    # Figure out the PV base name for the Link Node, given a crate_id. There is
    # one Link Node IOC per ATCA crate. The PV base name is:
    #
    #   MPLN:<LOCA>:MP<NUM>
    #
    # where:
    #   LOCA: is the sector where the crate is installed (e.g. LI00, LI10, LTU...)
    #   NUM: index of the Link Node within LOCA (following LCLS-I convention)
    #        example, for LI01 sector there are four crates:
    #        L2KG01-1925 -> MPLN:LI01:MP01 (lowest elevation within rack)
    #        L2KG01-1931 -> MPLN:LI01:MP02
    #        L2KG01-1937 -> MPLN:LI01:MP03 (highest elevation within rack)
    #        L2KG01-2037 -> MPLN:LI01:MP11
    #
    def getLinkNodePv(self, crate_id):
        return "MPLN:LI00:MP01"