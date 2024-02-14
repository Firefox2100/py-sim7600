import pytest
from numpy.testing import assert_equal

import py_sim7600
import tests
from py_sim7600.controller.v25ter import V25TERController, V25TERException


@pytest.fixture
def mock_v25ter_controller(mock_sim7600_device, request) -> V25TERController:
    controller = V25TERController(
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


class TestV25TERController:
    @pytest.mark.parametrize('mock_v25ter_controller', [(b'A/\r', b'\r\nOK\r\n')], indirect=True)
    def test_re_issue(self, mock_v25ter_controller):
        result = mock_v25ter_controller.re_issue()

        assert result == 'OK'

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATD1234567890;\r', b'\r\nOK\r\nVOICE CALL: BEGIN\r\n')],
                             indirect=True)
    def test_dial(self, mock_v25ter_controller):
        result = mock_v25ter_controller.dial(
            number='1234567890',
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATD>SM3;\r', b'\r\nOK\r\nVOICE CALL: BEGIN\r\n')],
                             indirect=True)
    def test_dial_from(self, mock_v25ter_controller):
        result = mock_v25ter_controller.dial_from(
            target=3,
            memory='SM',
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATD>2;\r', b'\r\nOK\r\nVOICE CALL: BEGIN\r\n')],
                             indirect=True)
    def test_dial_from_active_memory(self, mock_v25ter_controller):
        result = mock_v25ter_controller.dial_from(
            target=2,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATD>"Bob";\r', b'\r\nOK\r\nVOICE CALL: BEGIN\r\n')],
                             indirect=True)
    def test_dial_from_entry_name(self, mock_v25ter_controller):
        result = mock_v25ter_controller.dial_from(
            target='Bob',
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATA\r', b'\r\nVOICE CALL: BEGIN\r\nOK\r\n')], indirect=True)
    def test_answer(self, mock_v25ter_controller):
        result = mock_v25ter_controller.answer()

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATA\r', b'\r\nNO CARRIER\r\n')], indirect=True)
    def test_answer_no_call(self, mock_v25ter_controller):
        with pytest.raises(V25TERException):
            mock_v25ter_controller.answer()

    # @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATH\r', b'\r\nVOICE CALL: END: 001122\r\nOK\r\n')], indirect=True)
    # def test_disconnect(self, mock_v25ter_controller):
    #     result = mock_v25ter_controller.disconnect()
    #
    #     assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATS0=003\r', b'\r\nOK\r\n')], indirect=True)
    def test_auto_answer(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_auto_answer(
            times=3,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATS0?\r', b'\r\n003\r\nOK\r\n')], indirect=True)
    def test_check_auto_answer(self, mock_v25ter_controller):
        result = mock_v25ter_controller.check_auto_answer()

        assert result == 3

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'+++\r', b'\r\nOK\r\n')], indirect=True)
    def test_switch_to_command(self, mock_v25ter_controller):
        result = mock_v25ter_controller.switch_to_command()

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATO\r', b'\r\nCONNECT 115200\r\n')], indirect=True)
    def test_switch_to_data(self, mock_v25ter_controller):
        result = mock_v25ter_controller.switch_to_data()

        assert result

    def test_info(self, mock_v25ter_controller):
        result = mock_v25ter_controller.info()

        assert_equal(result, {
            'manufacturer': 'SIMCOM INCORPORATED',
            'model': 'SIMCOM_SIM7600C',
            'revision': 'SIM7600C _V1.0',
            'imei': 351602000330570,
            'capabilities': ['CGSM', 'FCLASS', 'DS'],
        })

    # def test_set_baud(self):
    #     pass
    #
    # def test_check_baud(self):
    #     pass
    #
    # def test_set_control_character(self):
    #     pass
    #
    # def test_check_control_character(self):
    #     pass
    #
    # def test_set_data_flow(self):
    #     pass
    #
    # def test_check_data_flow(self):
    #     pass
    #
    # def test_set_dcd_function(self):
    #     pass
    #
    # def test_enable_command_echo(self):
    #     pass
    #
    # def test_current_config(self):
    #     pass
    #
    # def test_set_dtr(self):
    #     pass
    #
    # def test_set_dsr(self):
    #     pass
    #
    # def test_set_result_format(self):
    #     pass
    #
    # def test_reset_config(self):
    #     pass
    #
    # def test_set_result_presentation(self):
    #     pass
    #
    # def test_set_connect_format(self):
    #     pass
