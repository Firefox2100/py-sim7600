"""
This file contains class to interface with the hardware directly. This file may raise SIM7600Exception,
remember to capture accordingly.
"""

import serial
import time
from py_sim7600.error import SIM7600Exception

# Attempt to import RPI.GPIO
try:
    import RPi.GPIO as GPIO
    is_rpi = True
except ImportError as e:
    is_rpi = False


class Device:
    """
    Class to communicate directly with SIM7600 device
    """

    def __init__(self, port: str, baud=115200):
        self.__port = port
        self.__is_rpi = is_rpi
        self.__serial = serial.Serial(port, baud)
        self.__serial.reset_input_buffer()
        self.__power_key = 6
        self.__is_on = not self.__is_rpi
        self.__buffer = ''

    def result(self) -> str:
        """
        Fetch the result from the buffer

        :return: Results
        """

        temp = self.__buffer
        self.__buffer = ''

        return temp

    def power_on(self):
        """
        Turn on the device

        :return: None
        """

        if self.__is_rpi:
            self.__buffer += "SIM7600 is starting...\n"
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
            self.__buffer += "SIM7600 is ready\n"
        else:
            raise SIM7600Exception('No GPIO access. Not on a Raspberry Pi?')

    def power_down(self):
        """
        Turn off the device

        :return: None
        """

        self.__buffer += "SIM7600 is shutting down...\n"
        GPIO.output(self.__power_key, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(self.__power_key, GPIO.LOW)
        time.sleep(18)
        self.__buffer += "SIM7600 is off\n"

    def send_without_result(self, command: str, back: str = None, timeout=5) -> bool:
        """
        Send a command to the device, without expecting a result

        :param command: Raw command to send to the string
        :param back: String expected to be in the successful result
        :param timeout: Optional. Timeout time in seconds
        :return: Boolean value
        """

        if not self.__is_on:
            raise SIM7600Exception("Device not on")

        self.__serial.write((command + "\r\n").encode())
        time.sleep(timeout)
        if self.__serial.in_waiting > 0:
            time.sleep(0.01)
            self.__buffer = self.__serial.read(self.__serial.in_waiting).decode()
        if self.__buffer != '':
            if back is not None and back not in self.__buffer:
                raise SIM7600Exception("Execution failed", self.__buffer)
            else:
                return True
        else:
            raise SIM7600Exception("Device timed out")

    def send(self, command: str, back: str = None, timeout=5) -> str:
        """
        Send a command to the device

        :param command: Raw command to send to the string
        :param back: String expected to be in the successful result
        :param timeout: Optional. Timeout time in seconds
        :return: Result string returned by the device
        """

        self.send_without_result(command, back, timeout)

        time.sleep(0.01)

        return self.result()
