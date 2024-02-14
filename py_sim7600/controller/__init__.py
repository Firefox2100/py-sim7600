from py_sim7600.exceptions import ControllerException
from py_sim7600.device import Device


class DeviceController:
    def __init__(self,
                 port: str = None,
                 baud: int = None,
                 device: Device = None,
                 ):
        if device is not None:
            self.device = device
        else:
            self.device = Device(port, baud)

        self.verify()

    def open(self):
        self.device.open()

    def close(self):
        self.device.close()

    def verify(self):
        """
        Verify that the interface is connected to a SIMCom device,
        and that the device is functioning properly.
        """

        if type(self.device) is Device:
            # Using the generic Device class
            raise ControllerException("Controller can only be initialized with a subclass of Device")

        return self.device.verify()
