import pytest
from numpy.testing import assert_equal

import py_sim7600
import tests
from py_sim7600.controller.call_control import CallController, CallControlException


@pytest.fixture
def mock_call_controller(mock_sim7600_device, request) -> CallController:
    controller = CallController(
        device=mock_sim7600_device,
    )

    if hasattr(request, 'param'):
        payload = {
            'input': request.param[0],
            'output': request.param[1],
        }

        controller.device._Device__serial.add_response(payload)

    controller.open()

    yield controller


class TestCallController:
    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CVHU=0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_control_voice_hangup(self, mock_call_controller):
        result = mock_call_controller.set_control_voice_hangup(disconnect_ath=True)

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CVHU?\r', b'\r\n+CVHU: 0\r\nOK\r\n')], indirect=True)
    def test_check_control_voice_hangup(self, mock_call_controller):
        result = mock_call_controller.check_control_voice_hangup()

        assert result
