import pytest
from unittest.mock import patch

from py_sim7600.device import Device
from py_sim7600.device.sim7600 import SIM7600Device

from . import MockSerial


@pytest.fixture
def mock_serial():
    with patch('serial.Serial', new=MockSerial) as mock_serial:
        yield mock_serial


@pytest.fixture
def mock_device(mock_serial) -> Device:
    port = '/dev/ttyUSB0'
    baud = 115200
    device = Device(port, baud)

    device._Device__serial.add_response(
        {
            'input': b'AT\r',
            'output': b'\r\nOK\r\n',
        }
    )

    yield device


@pytest.fixture
def mock_sim7600_device(mock_serial) -> SIM7600Device:
    port = '/dev/ttyUSB0'
    baud = 115200
    device = SIM7600Device(port, baud)

    device._Device__serial.add_response(
        {
            'input': b'AT\r',
            'output': b'\r\nOK\r\n',
        }
    )

    device._Device__serial.add_response(
        {
            'input': b'ATI\r',
            'output': b'\r\nManufacturer: SIMCOM INCORPORATED\rModel: SIMCOM_SIM7600C\rRevision: SIM7600C '
                      b'_V1.0\rIMEI: 351602000330570\r+GCAP: +CGSM,+FCLASS,+DS\rOK\r\n',
        }
    )

    yield device
