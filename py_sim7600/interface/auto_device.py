import re
import serial.tools.list_ports

from py_sim7600.exceptions import AutoDeviceException
from py_sim7600.device import Device


class AutoDevice:
    """
    An interface to automatically construct a Device class (or
    subclass) either by searching for a device or by providing
    a device's serial port.
    """

    def search(self):
        """
        Search all serial ports for a device.

        Note that this will attempt to connect to those ports,
        and send AT commands to them to identify if they are
        a SIMCom device. This may interfere with other devices
        connected to the serial port.
        """

        devices = []
        port_info = serial.tools.list_ports.comports()

        for port in port_info:
            try:
                device = self.identify(port.device)

                if device:
                    devices.append(device)
            except AutoDeviceException:
                pass

        return devices

    @staticmethod
    def identify(port: str) -> Device | None:
        """
        Identify a device on the given port, and return a
        Device object.

        :param port: The port to identify the device on
        :return: A Device object, or None if the device is not
                 a usable SIMCom device
        :rtype: Device or None
        :raises AutoDeviceException: If the device could not be
                                     identified
        """

        try:
            d = Device(port)

            if not d.verify():
                # Did not respond to AT command, not an AT interface modem
                return None

            result = d.send(
                command='ATI',
                pattern='\r\n',
                back='OK',
            )

            if not result:
                # Did not respond to ATI command, or response is not parseable
                return None

            pattern = r'Manufacturer:[.]*SIMCOM'
            match = re.search(pattern, result)

            if not match:
                # Not a SIMCom device
                return None

            pattern = r'Model: ([A-Z0-9_]+)'
            model_identifier = re.search(pattern, result).group(1)

            if 'SIM7600' in model_identifier:
                from py_sim7600.device.sim7600 import SIM7600Device
                return SIM7600Device(port)

            # Cannot identify the model, but it is a SIMCom device
            return d
        except Exception as e:
            raise AutoDeviceException(
                message=f'Failed to identify device on port {port}',
                errors=str(e),
            )
