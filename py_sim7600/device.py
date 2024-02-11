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
        self.__buffer = ''

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

    def result(self) -> str:
        """
        Fetch the result from the buffer

        :return: Results
        :rtype: str
        """

        temp = self.__buffer
        self.__buffer = ''

        return temp

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

    def send_without_result(self, command: str, back: str = None, timeout=5) -> bool:
        """
        Send a command to the device, without expecting a result

        :param command: Raw command to send to the string
        :param back: String expected to be in the successful result
        :param timeout: Optional. Timeout time in seconds
        :return: True if successful
        :rtype: bool
        :raises DeviceException: If the device is off or the command fails
        """

        if not self.__is_on:
            raise DeviceException("Device not on")

        self.__serial.write((command + "\r\n").encode())
        time.sleep(timeout)
        if self.__serial.in_waiting > 0:
            time.sleep(0.01)
            self.__buffer = self.__serial.read(self.__serial.in_waiting).decode()
        if self.__buffer != '':
            if back is not None and back not in self.__buffer:
                raise DeviceException("Execution failed", self.__buffer)
            else:
                return True
        else:
            raise DeviceException("Device timed out")

    def send(self, command: str, back: str = None, timeout=5) -> str:
        """
        Send a command to the device

        :param command: Raw command to send to the string
        :param back: String expected to be in the successful result
        :param timeout: Optional. Timeout time in seconds
        :return: Result string returned by the device
        :rtype: str
        """

        self.send_without_result(command, back, timeout)

        time.sleep(0.01)

        return self.result()
