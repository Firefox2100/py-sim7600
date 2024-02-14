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


class ControllerException(SIM7600Exception):
    """
    Exception raised by the base Controller class
    """
    pass


class V25TERException(ControllerException):
    """
    Exception raised by V25TER commands
    """
    pass


class StatusControlException(ControllerException):
    """
    Exception raised by status control commands
    """
    pass


class NetworkException(ControllerException):
    """
    Exception raised by network commands
    """
    pass


class CallControlException(ControllerException):
    """
    Exception raised by call control commands
    """
    pass


class PhonebookException(ControllerException):
    """
    Exception raised by phonebook commands
    """
    pass


class SIMApplicationToolkitException(ControllerException):
    """
    Exception raised by phonebook commands
    """
    pass


class GPRSException(ControllerException):
    """
    Exception raised by phonebook commands
    """
    pass


class DeviceException(SIM7600Exception):
    """
    Exception raised by Device class
    """
    pass
