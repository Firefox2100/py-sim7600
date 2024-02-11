"""
This file contains classes related to phonebook commands. This file may raise PhonebookException,
remember to capture accordingly.
"""

from py_sim7600.device import Device
from py_sim7600.exceptions import PhonebookException


class Phonebook:
    """
    AT Commands for Phonebook
    """

    @staticmethod
    def select_memory(device: Device) -> str:
        """
        Select Phonebook memory storage

        Corresponding command: AT+CPBS

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises PhonebookException:
        """
        raise NotImplementedError

    @staticmethod
    def read_entry(device: Device) -> str:
        """
        Read Phonebook entries

        Corresponding command: AT+CPBR

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises PhonebookException:
        """
        raise NotImplementedError

    @staticmethod
    def find_entry(device: Device) -> str:
        """
        Find Phonebook entries

        Corresponding command: AT+CPBF

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises PhonebookException:
        """
        raise NotImplementedError

    @staticmethod
    def write_entry(device: Device) -> str:
        """
        Write Phonebook entry

        Corresponding command: AT+CPBW

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises PhonebookException:
        """
        raise NotImplementedError

    @staticmethod
    def subscriber(device: Device) -> str:
        """
        Subscriber number

        Corresponding command: AT+CNUM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises PhonebookException:
        """
        raise NotImplementedError
