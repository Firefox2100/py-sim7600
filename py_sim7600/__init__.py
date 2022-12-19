__version__ = "0.1.0-pre-alpha"

from py_sim7600.device import Device
import py_sim7600.error as error
from py_sim7600.v25ter import V25TER


class SIM:
    def __init__(self, port="/dev/ttyACM0"):
        self.device = Device(port=port)
