from py_sim7600.device import Device


class Interface:
    def __init__(self, port="/dev/ttyACM0", device: Device = None):
        if device is not None:
            self.device = device
        else:
            self.device = Device(port=port)
