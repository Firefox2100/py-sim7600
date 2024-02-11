"""
This file contains custom exception types for SIM7600 library.
"""


class SIM7600Exception(Exception):
    """
    Base exception for SIM7600 library
    """

    def __init__(self, message: str = None, errors=''):
        """
        Constructor

        :param message: Exception message
        :param errors: Additional error information
        """
        super().__init__(message)

        self.errors = errors

    def __str__(self):
        return super().__str__() + f" {self.errors}"


class V25TERException(SIM7600Exception):
    """
    Exception raised by V25TER commands
    """
    pass


class StatusControlException(SIM7600Exception):
    """
    Exception raised by status control commands
    """
    pass


class NetworkException(SIM7600Exception):
    """
    Exception raised by network commands
    """
    pass


class CallControlException(SIM7600Exception):
    """
    Exception raised by call control commands
    """
    pass


class PhonebookException(SIM7600Exception):
    """
    Exception raised by phonebook commands
    """
    pass


class SIMApplicationToolkitException(SIM7600Exception):
    """
    Exception raised by phonebook commands
    """
    pass


class GPRSException(SIM7600Exception):
    """
    Exception raised by phonebook commands
    """
    pass


class DeviceException(SIM7600Exception):
    """
    Exception raised by Device class
    """
    pass
