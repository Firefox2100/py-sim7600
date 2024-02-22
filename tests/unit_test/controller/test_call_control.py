import pytest
from numpy.testing import assert_equal

import tests

from py_sim7600.model import enums
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
    def test_get_control_voice_hangup(self, mock_call_controller):
        result = mock_call_controller.get_control_voice_hangup()

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CHUP\r', b'\r\nVOICE CALL:END: 000017\r\nOK\r\n')],
                             indirect=True)
    def test_hang_up(self, mock_call_controller):
        result = mock_call_controller.hang_up()

        assert result == 17

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CHUP\r', b'\r\nOK\r\n')], indirect=True)
    def test_hang_up_no_call(self, mock_call_controller):
        result = mock_call_controller.hang_up()

        assert result == 0

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CBST=0,0,1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_bearer_type(self, mock_call_controller):
        result = mock_call_controller.set_bearer_type(
            bearer_speed=enums.BearerServiceSpeed.AUTO,
            bearer_name=enums.BearerServiceName.ASYNC_MODEM,
            bearer_ce=enums.BearerServiceConnectionElement.NON_TRANSPARENT,
        )

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CBST?\r', b'\r\n+CBST: 0,0,1\r\nOK\r\n')], indirect=True)
    def test_get_bearer_type(self, mock_call_controller):
        result = mock_call_controller.get_bearer_type()

        assert_equal(
            result,
            (
                enums.BearerServiceSpeed.AUTO,
                enums.BearerServiceName.ASYNC_MODEM,
                enums.BearerServiceConnectionElement.NON_TRANSPARENT,
            )
        )

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CRLP=61,61,48,6,0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_rlp_parameter(self, mock_call_controller):
        result = mock_call_controller.set_rlp_parameter(
            rlp_version=0,
            iws=61,
            mws=61,
            ack_timer=48,
            retry_times=6,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_call_controller',
        [(b'AT+CRLP?\r', b'\r\n+CRLP: 61,61,48,6,0\r\n+CRLP: 0,61,48,6,1\r\n+CRLP: 240,240,52,6,2\r\nOK\r\n')],
        indirect=True)
    def test_get_rlp_parameter(self, mock_call_controller):
        result = mock_call_controller.get_rlp_parameter()

        assert_equal(
            result,
            [
                (61, 61, 48, 6, 0),
                (0, 61, 48, 6, 1),
                (240, 240, 52, 6, 2),
            ]
        )

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CR=1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_service_report(self, mock_call_controller):
        result = mock_call_controller.set_service_report(
            report=True,
        )

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CR?\r', b'\r\n+CR: 1\r\nOK\r\n')], indirect=True)
    def test_get_service_report(self, mock_call_controller):
        result = mock_call_controller.get_service_report()

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CRC=1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_result_code(self, mock_call_controller):
        result = mock_call_controller.set_result_code(
            extended_format=True,
        )

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CRC?\r', b'\r\n+CRC: 1\r\nOK\r\n')], indirect=True)
    def test_get_result_code(self, mock_call_controller):
        result = mock_call_controller.get_result_code()

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CLCC=1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_list_call(self, mock_call_controller):
        result = mock_call_controller.set_list_call(
            auto_report=True,
        )

        assert result

    @pytest.mark.parametrize('mock_call_controller', [(b'AT+CLCC?\r', b'\r\n+CLCC: 1\r\nOK\r\n')], indirect=True)
    def test_get_list_call(self, mock_call_controller):
        result = mock_call_controller.get_list_call()

        assert result
