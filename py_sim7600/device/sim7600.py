"""
This file contains class to interface with the hardware directly.

This file may raise DeviceException, remember to capture accordingly.
"""

from . import Device


class SIM7600Device(Device):
    """
    This class is a wrapper around the Device class to provide SIM7600 specific functionality
    """

    def read_full_response(self, pattern='\r\n', timeout=2) -> str | None:
        return super().read_full_response(pattern, timeout)

    def send(self, command: str, pattern='\r\n', back: str = None, error_pattern: list[str] = None, timeout=2) -> str | None:
        return super().send(
            command=command,
            pattern=pattern,
            back=back,
            timeout=timeout,
            error_pattern=error_pattern,
        )

    def verify(self) -> bool:
        if not super().verify():
            return False

        was_open = self.is_open

        if not was_open:
            self.open()

        # Get the identification of the device
        result = self.send('ATI')

        if not was_open:
            self.close()

        return 'SIM7600' in result
