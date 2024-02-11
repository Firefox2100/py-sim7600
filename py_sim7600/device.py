"""
This file contains class to interface with the hardware directly. This file may raise SIM7600Exception,
remember to capture accordingly.
"""

import serial
import time
from py_sim7600.exceptions import DeviceException

# Attempt to import RPI.GPIO
try:
    import RPi.GPIO as GPIO
    is_rpi = True
except ImportError:
    is_rpi = False


class Device:
    """
    Class to communicate directly with SIM7600 device
    """

    def __init__(self, port: str, baud=115200):
        """
        Constructor

        :param port: Port to connect to
        :param baud: Optional. Baud rate of the connection
        """
        self.__port = port
        self.__is_rpi = is_rpi
        self.__serial = serial.Serial(port, baud)
        self.__serial.reset_input_buffer()
        self.__power_key = 6
        self.__is_on = not self.__is_rpi

    def open(self):
        """
        Open the serial connection

        :return: None
        :raises DeviceException: If the connection fails
        """

        try:
            self.__serial.open()
        except serial.SerialException as e:
            raise DeviceException() from e

    def close(self):
        """
        Close the serial connection

        :return: None
        """

        self.__serial.close()

    def power_on(self):
        """
        Turn on the device

        :return: None
        :raises DeviceException: If the device is already on or no GPIO access
        """

        if self.__is_rpi:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.__power_key, GPIO.OUT)
            time.sleep(0.1)
            GPIO.output(self.__power_key, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(self.__power_key, GPIO.LOW)
            time.sleep(20)
            self.__serial.reset_input_buffer()
            self.__is_on = True
        else:
            raise DeviceException('No GPIO access. Not on a Raspberry Pi?')

    def power_down(self) -> None:
        """
        Turn off the device

        :return: None
        :raises DeviceException: If the device is already off or no GPIO access
        """

        if self.__is_rpi:
            if not self.__is_on:
                raise DeviceException("Device not on")

            GPIO.output(self.__power_key, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(self.__power_key, GPIO.LOW)
            time.sleep(18)
        else:
            raise DeviceException('No GPIO access. Not on a Raspberry Pi?')

    def read_full_response(self, timeout=5, pattern='\r\n') -> str:
        """
        Read the full response from the device.

        SIM7600 responses are in the format of <CR><LF>...<CR><LF>,
        so this function looks for a starting and ending pattern to
        determine when the response is complete.
        """

        start_time = time.time()
        accumulated_data = ''
        response_started = False

        time.sleep(0.1)

        # while True:
        while time.time() - start_time < timeout:
            if self.__serial.in_waiting > 0:
                accumulated_data += self.__serial.read(self.__serial.in_waiting).decode()
                if pattern in accumulated_data:
                    response_started = True
                if response_started and accumulated_data.endswith(pattern) and accumulated_data != pattern:
                    # Strip the beginning and ending pattern
                    return accumulated_data[len(pattern):-len(pattern)]

            time.sleep(0.01)

        raise DeviceException("Device read timeout")

    def send(self, command: str, back: str = None, timeout=5) -> str:
        """
        Send a command to the device, without expecting a result

        :param command: Raw command to send to the string
        :param back: String expected to be in the successful result
        :param timeout: Optional. Timeout time in seconds
        :return: The result string returned by the device
        :rtype: bool
        :raises DeviceException: If the device is off or the command fails
        """

        if not self.__is_on:
            raise DeviceException("Device not on")

        self.__serial.write((command + "\r").encode())
        response = self.read_full_response(timeout)

        if response is not None:
            if back is not None and back not in response:
                raise DeviceException("Execution failed", response)
            else:
                return response
        else:
            raise DeviceException("Device returned no response")
