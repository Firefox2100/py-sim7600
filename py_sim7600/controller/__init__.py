from py_sim7600.device import Device


class SIM7600Controller:
    def __init__(self,
                 port: str = None,
                 baud: int = None,
                 device: Device = None,
                 ):
        if device is not None:
            self.device = device
        else:
            self.device = Device(port, baud)
