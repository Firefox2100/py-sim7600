"""
This file contains custom exception types for SIM7600 library.
"""


class SIM7600Exception(Exception):
    """
    Exception raised by SIM7600 device commands
    """

    def __init__(self, message: str, errors=''):
        super().__init__(message)

        if errors != "":
            self.errors = errors
            print("Error:")
            print(errors)


class V25TERException(Exception):
    """
    Exception raised by V25TER commands
    """

    def __init__(self, message: str, errors=''):
        super().__init__(message)

        if errors != "":
            self.errors = errors
            print("Error:")
            print(errors)


class StatusControlException(Exception):
    """
    Exception raised by status control commands
    """

    def __init__(self, message: str, errors=''):
        super().__init__(message)

        if errors != "":
            self.errors = errors
            print("Error:")
            print(errors)


class CallControlException(Exception):
    """
    Exception raised by call control commands
    """

    def __init__(self, message: str, errors=''):
        super().__init__(message)

        if errors != "":
            self.errors = errors
            print("Error:")
            print(errors)
