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
        self.port = port
        self.is_rpi = is_rpi
        self.serial = serial.Serial(port, baud)
        self.serial.flushInput()
        self.power_key = 6
        self.is_on = not self.is_rpi
        self.buffer = ''

    def result(self) -> str:
        """
        Fetch the result from the buffer

        :return: Results
        """

        temp = self.buffer
        self.buffer = ''

        return temp

    def power_on(self):
        """
        Turn on the device

        :return: None
        """

        if self.is_rpi:
            self.buffer += "SIM7600 is starting...\n"
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.power_key, GPIO.OUT)
            time.sleep(0.1)
            GPIO.output(self.power_key, GPIO.HIGH)
            time.sleep(2)
            GPIO.output(self.power_key, GPIO.LOW)
            time.sleep(20)
            self.serial.flushInput()
            self.is_on = True
            self.buffer += "SIM7600 is ready\n"
        else:
            raise SIM7600Exception('No GPIO access. Not on a Raspberry Pi?')

    def power_down(self):
        """
        Turn off the device

        :return: None
        """

        self.buffer += "SIM7600 is shutting down...\n"
        GPIO.output(self.power_key, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(self.power_key, GPIO.LOW)
        time.sleep(18)
        self.buffer += "SIM7600 is off\n"

    def send(self, command: str, back: str, timeout=5) -> bool:
        """
        Send a command to the device

        :param command: Raw command to send to the string
        :param back: String expected to be in the successful result
        :param timeout: Optional. Timeout time in seconds
        :return: Boolean value
        """
        if not self.is_on:
            raise SIM7600Exception("Device not on")

        self.serial.write((command + "\r\n").encode())
        time.sleep(timeout)
        if self.serial.inWaiting():
            time.sleep(0.01)
            self.buffer = self.serial.read(self.serial.inWaiting()).decode()
        if self.buffer != '':
            if back not in self.buffer:
                raise SIM7600Exception("Execution failed", self.buffer)
            else:
                return True
        else:
            raise SIM7600Exception("Device timed out")
