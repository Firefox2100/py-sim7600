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
    def test_get_function(self, mock_status_controller):
        result = mock_status_controller.get_function()

        assert result == enums.PhoneFunctionalityLevel.FULL

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CPIN=123456\r', b'\r\nOK\r\n')], indirect=True)
    def test_enter_pin(self, mock_status_controller):
        mock_status_controller.device._Device__serial.add_response({
            'input': b'AT+CPIN?\r',
            'output': b'\r\n+CPIN: SIM PIN\r\nOK\r\n',
        })

        result = mock_status_controller.enter_pin('123456')

        assert result

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CPIN=123456\r', b'\r\nOK\r\n')], indirect=True)
    def test_enter_pin_with_no_need(self, mock_status_controller):
        mock_status_controller.device._Device__serial.add_response({
            'input': b'AT+CPIN?\r',
            'output': b'\r\n+CPIN: READY\r\nOK\r\n',
        })

        with pytest.raises(StatusControlException):
            mock_status_controller.enter_pin('123456')

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CPIN=654321,123456\r', b'\r\nOK\r\n')], indirect=True)
    def test_enter_pin_and_puk(self, mock_status_controller):
        mock_status_controller.device._Device__serial.add_response({
            'input': b'AT+CPIN?\r',
            'output': b'\r\n+CPIN: SIM PUK\r\nOK\r\n',
        })

        result = mock_status_controller.enter_pin(
            pin='123456',
            puk='654321',
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CICCID\r', b'\r\n+ICCID: 898600700907A6019125\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_iccid(self, mock_status_controller):
        result = mock_status_controller.get_iccid()

        assert result == '898600700907A6019125'

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+SPIC\r', b'\r\n+SPIC: 3,10,0,10\r\nOK\r\n')],
        indirect=True,
    )
    def test_pin_times(self, mock_status_controller):
        result = mock_status_controller.pin_times()

        assert_equal(result, (3, 10, 0, 10))

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CSPN?\r', b'\r\n+CSPN: "CMCC",0\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_provider(self, mock_status_controller):
        result = mock_status_controller.get_provider()

        assert_equal(result, ('CMCC', 0))
