import pytest
from numpy.testing import assert_equal

from py_sim7600.controller.status_control import StatusController, StatusControlException
from py_sim7600.model import enums


@pytest.fixture
def mock_status_controller(mock_sim7600_device, request) -> StatusController:
    controller = StatusController(
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


class TestStatusController:
    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CFUN=0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_function(self, mock_status_controller):
        mock_status_controller.device._Device__serial.add_response({
            'input': b'AT+CFUN?\r',
            'output': b'\r\n+CFUN: 1\r\nOK\r\n',
        })

        result = mock_status_controller.set_function(enums.PhoneFunctionalityLevel.MINIMUM)

        assert result

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CFUN=0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_function_restart_required(self, mock_status_controller):
        mock_status_controller.device._Device__serial.add_response({
            'input': b'AT+CFUN?\r',
            'output': b'\r\n+CFUN: 7\r\nOK\r\n',
        })

        with pytest.raises(StatusControlException):
            mock_status_controller.set_function(enums.PhoneFunctionalityLevel.MINIMUM)

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CFUN?\r', b'\r\n+CFUN: 1\r\nOK\r\n')], indirect=True)
    def test_set_function(self, mock_status_controller):
        result = mock_status_controller.get_function()

        assert result == enums.PhoneFunctionalityLevel.FULL
