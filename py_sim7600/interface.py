from py_sim7600.device import Device


class Interface:
    def __init__(self, port="/dev/ttyACM0"):
        self.device = Device(port=port)
