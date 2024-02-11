import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from py_sim7600.device import Device, DeviceException

from . import MockSerial


@pytest.fixture
def mock_serial():
    with patch('serial.Serial', new=MockSerial) as mock_serial:
        yield mock_serial


@pytest.fixture
def mock_device(mock_serial):
    port = '/dev/ttyUSB0'
    baud = 115200
    device = Device(port, baud)
    yield device


class TestDevice:
    def test_init(self, mock_serial):
        port = '/dev/ttyUSB0'
        baud = 115200
        device = Device(port, baud)

        assert device._Device__port == port
        assert device._Device__is_rpi == False
        assert device._Device__power_key == 6
        assert device._Device__is_on == True
        assert device._Device__buffer == ''

        assert isinstance(device._Device__serial, MockSerial)

        assert device._Device__serial._port == port
        assert device._Device__serial._baudrate == baud
        assert device._Device__serial._input_buffer == b''

    def test_open(self, mock_device):
        mock_device.open()

        assert mock_device._Device__serial._is_open

        with pytest.raises(DeviceException):
            mock_device.open()

    def test_close(self, mock_device):
        mock_device.open()
        mock_device.close()

        assert not mock_device._Device__serial._is_open

    def test_send_without_result(self, mock_device):
        mock_device.open()
        mock_device._Device__serial.add_response({
            'input': b'AT\r\n',
            'output': b'OK\r\n',
        })

        mock_device.send_without_result('AT', timeout=0)

        assert mock_device._Device__serial._output_buffer == b'AT\r\n'
        assert mock_device._Device__serial._input_buffer == b''
        assert mock_device._Device__buffer == 'OK\r\n'

    def test_result(self, mock_device):
        mock_device._Device__buffer = 'OK\r\n'

        result = mock_device.result()

        assert result == 'OK\r\n'

    def test_send(self, mock_device):
        mock_device.open()
        mock_device._Device__serial.add_response({
            'input': b'AT\r\n',
            'output': b'OK\r\n',
        })

        result = mock_device.send('AT', timeout=0)

        assert result == 'OK\r\n'
