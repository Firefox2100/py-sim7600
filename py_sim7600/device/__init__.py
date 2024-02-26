"""
This module contains the classes and functions to interact with a SIMCom device.
"""

import serial
import time
import re
from threading import Semaphore

from py_sim7600.exceptions import DeviceException

# Attempt to import RPI.GPIO
try:
    import RPi.GPIO as GPIO
    is_rpi = True
except ImportError:
    is_rpi = False


class Device:
    """
    Class to communicate directly with SIMCom device
    """

    __urc: list[str] = []           # Unsolicited responses
    __sem = Semaphore()             # Semaphore to prevent multiple threads from writing to the device

    def __init__(self, port: str, baud=115200, serial_device: serial.Serial = None):
        """
        Class to communicate directly with SIMCom device

        :param port: Port to connect to
        :param baud: Optional. Baud rate of the connection
        :param serial_device: Optional. A serial device to use
        """
        self.__port = port
        self.__is_rpi = is_rpi

        if serial_device is not None:
            self.__serial = serial_device
        else:
            self.__serial = serial.Serial(port, baud)
        self.__serial.reset_input_buffer()
        self.__power_key = 6
        self.__is_on = not self.__is_rpi

    def verify(self) -> bool:
        """
        Verify that this is indeed a SIMCom device

        :return: True if the device is verified, False otherwise
        :rtype: bool
        """

        was_open = self.__serial.is_open

        if not was_open:
            self.open()

        with self.__sem:
            self.__serial.write(b'AT\r')
            response = self.read_full_response('\r\n')

        if not was_open:
            self.close()

        return 'OK' in response

    @property
    def is_open(self) -> bool:
        """
        Check if the serial connection is open

        :return: True if the connection is open, False otherwise
        :rtype: bool
        """

        return self.__serial.is_open

    def open(self) -> None:
        """
        Open the serial connection

        :return: None
        :raises DeviceException: If the port fails to open
        """

        try:
            self.__serial.open()
        except serial.SerialException as e:
            raise DeviceException() from e

    def close(self) -> None:
        """
        Close the serial connection

        :return: None
        """
        try:
            self.__serial.close()
        except serial.SerialException:
            pass

    def power_on(self) -> None:
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

    def read_full_response(self, pattern: str, timeout=5) -> list[str] | None:
        """
        Read the full response from the device.

        :param timeout: Optional. Timeout time in seconds
        :param pattern: The pattern that encapsulates the response
        :return: The response string. None if no response is received
        :rtype: str | None
        :raises DeviceException: If the device read times out
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
                    # The response may contain the pattern in the middle, wait a bit more
                    current_length = len(accumulated_data)
                    time.sleep(0.1)
                    accumulated_data += self.__serial.read(self.__serial.in_waiting).decode()

                    if len(accumulated_data) == current_length:
                        # Do a look-ahead match to segment one or multiple responses
                        escaped_pattern = re.escape(pattern)

                        re_pattern = re.compile(
                            f'{escaped_pattern}(.+?){escaped_pattern}(?={escaped_pattern}|$)',
                            re.DOTALL
                        )

                        matches = re_pattern.findall(accumulated_data)

                        if matches:
                            return matches
                        else:
                            return None
                    else:
                        continue

            time.sleep(0.01)

        raise DeviceException("Device read timeout")

    def send(self, command: str, pattern: str, back: str = None, error_pattern: list[str] = None, timeout=5) -> str:
        """
        Send a command to the device, and check for a successful response.

        :param command: Raw command to send to the string
        :param back: String expected to be in the successful result
        :param error_pattern: Optional. The response that should be considered an error
        :param timeout: Optional. Timeout time in seconds
        :param pattern: Optional. The pattern that encapsulates the response
        :return: The result string returned by the device
        :rtype: str
        :raises DeviceException: If the device is off or the command fails
        """

        if not self.__is_on:
            raise DeviceException("Device not on")

        with self.__sem:
            try:
                self.__serial.write((command + "\r").encode())
                response = self.read_full_response(pattern, timeout)
            except Exception as e:
                raise DeviceException() from e

        result_message = None
        error_message = ''

        if response is not None:
            for message in response:
                if error_pattern is not None and any([error in message for error in error_pattern]):
                    error_message = message
                    continue

                if result_message is not None:
                    self.__urc.append(message)
                    continue

                if back is not None and back in message:
                    result_message = message
                    continue

                if back is None:
                    # Treat the first response as the result
                    result_message = message
                    continue

                self.__urc.append(message)

            if error_message:
                raise DeviceException(f"Device returned error: {error_message}")

            if result_message is not None:
                return result_message

        raise DeviceException("Device returned no valid response")

    @property
    def urc(self, clear=True) -> list[str]:
        """
        Get the unsolicited responses from the device

        :return: The spontaneous responses
        :rtype: list[str]
        """

        # Read the device again to get more spontaneous responses
        with self.__sem:
            try:
                matches = self.read_full_response('\r\n')
                if matches is not None:
                    self.__urc.extend(matches)
            except DeviceException:
                pass

        responses = []

        if clear:
            # No thread lock here, so the results are popped
            while self.__urc:
                responses.append(self.__urc.pop(0))
        else:
            responses = self.__urc

        return responses

    @classmethod
    def set_lock(cls, lock):
        cls.__sem = lock
