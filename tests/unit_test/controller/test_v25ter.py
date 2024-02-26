import pytest
from numpy.testing import assert_equal

from py_sim7600.controller.v25ter import V25TERController, V25TERException
from py_sim7600.model import enums


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
    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT"\r', b'\r\nOK\r\n')], indirect=True)
    def test_command_with_timeout(self, mock_v25ter_controller):
        """
        Test the timeout for a command by sending a command that will not be responded to.

        It's at the beginning to allow pytest-xdist to run this one first.
        """

        with pytest.raises(V25TERException):
            mock_v25ter_controller.re_issue()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.dial(
                number='1234567890',
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.dial_from(
                target=3,
                memory=enums.PhonebookStorage.SIM_PHONEBOOK,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.answer()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.switch_to_command()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.switch_to_data()

        # ATI is not tested, as the command will always be responded to

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_baud(
                baud=9600,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_baud()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_control_character(
                format_control=enums.ControlCharacterFormat.D8S1,
                parity=enums.ControlCharacterParity.NONE,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_control_character()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_data_flow(
                rts=True,
                cts=True,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_data_flow()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_dcd_function(
                dcd=1,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.enable_command_echo(True)

        with pytest.raises(V25TERException):
            mock_v25ter_controller.current_config()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_dtr(
                dtr=1,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_dsr(
                always_on=True,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_result_format(
                verbose=True,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.reset_config()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_result_presentation(
                transmit=True,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_connect_format(
                mode=1,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_connect_protocol(
                report=False,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_connect_speed(
                report_serial=False,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.save_config()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.restore_config()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_manufacturer()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_model()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_revision()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_serial()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.set_te_charset(
                char_set=enums.TECharacterSet.IRA,
            )

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_te_charset()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_international_subscriber()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_another_subscriber()

        with pytest.raises(V25TERException):
            mock_v25ter_controller.get_capabilities()

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'A/\r', b'\r\nOK\r\n')], indirect=True)
    def test_re_issue(self, mock_v25ter_controller):
        result = mock_v25ter_controller.re_issue()

        assert result == 'OK'

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'A/\r', b'\r\nOK\r\n\r\nAnother response\r\n')], indirect=True)
    def test_re_issue_with_spontaneous_response(self, mock_v25ter_controller):
        result = mock_v25ter_controller.re_issue()

        assert result == 'OK'
        assert mock_v25ter_controller.device.urc == ['Another response']

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATD1234567890;\r', b'\r\nOK\r\nVOICE CALL: BEGIN\r\n')],
                             indirect=True)
    def test_dial(self, mock_v25ter_controller):
        result = mock_v25ter_controller.dial(
            number='1234567890',
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATD1234567890;\r', b'\r\nNO CARRIER\r\n')], indirect=True)
    def test_dial_fail_with_no_carrier(self, mock_v25ter_controller):
        with pytest.raises(V25TERException):
            mock_v25ter_controller.dial(
                number='1234567890',
            )

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATD>SM3;\r', b'\r\nOK\r\nVOICE CALL: BEGIN\r\n')],
                             indirect=True)
    def test_dial_from(self, mock_v25ter_controller):
        result = mock_v25ter_controller.dial_from(
            target=3,
            memory=enums.PhonebookStorage.SIM_PHONEBOOK,
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
    def test_get_auto_answer(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_auto_answer()

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

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+IPR=9600\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_baud(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_baud(
            baud=9600,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+IPR?\r', b'\r\n+IPR: 9600\r\nOK\r\n')], indirect=True)
    def test_get_baud(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_baud()

        assert result == 9600

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+ICF=3\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_control_character(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_control_character(
            format_control=enums.ControlCharacterFormat.D8S1,
            parity=enums.ControlCharacterParity.NONE,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+ICF?\r', b'\r\n+ICF: 3,3\r\nOK\r\n')], indirect=True)
    def test_get_control_character(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_control_character()

        assert_equal(result, (enums.ControlCharacterFormat.D8S1, enums.ControlCharacterParity.NONE))

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+IFC=2,2\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_data_flow(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_data_flow(
            rts=True,
            cts=True,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+IFC?\r', b'\r\n+IFC: 2,2\r\nOK\r\n')], indirect=True)
    def test_get_data_flow(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_data_flow()

        assert_equal(result, (True, True))

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT&C1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_dcd_function(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_dcd_function(
            dcd=1,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATE1\r', b'\r\nOK\r\n')], indirect=True)
    def test_enable_command_echo(self, mock_v25ter_controller):
        result = mock_v25ter_controller.enable_command_echo(True)

        assert result

    @pytest.mark.parametrize(
        'mock_v25ter_controller',
        [
            (
                b'AT&V\r',
                b'\r\n&C: 2; &D: 2; &F: 0; E: 1; L: 0; M: 0; Q: 0; V: 1; X: 0; Z: 0; S0: 0;\r\nS3: 13; S4: 10; S5: 8; '
                b'S6: 2; S7: 50; S8: 2; S9: 6; S10: 14; S11: 95;\r\n+FCLASS: 0; +ICF: 3,3; +IFC: 2,2; +IPR: 115200; '
                b'+DR: 0; +DS: 0,0,2048,6;\r\n+WS46: 12; +CBST: 0,0,1;\r\nOK\r\n'
            )
        ],
        indirect=True,
    )
    def test_current_config(self, mock_v25ter_controller):
        result = mock_v25ter_controller.current_config()

        assert_equal(
            result,
            {
                '&C': 2,
                '&D': 2,
                '&F': 0,
                'E': 1,
                'L': 0,
                'M': 0,
                'Q': 0,
                'V': 1,
                'X': 0,
                'Z': 0,
                'S0': 0,
                'S3': 13,
                'S4': 10,
                'S5': 8,
                'S6': 2,
                'S7': 50,
                'S8': 2,
                'S9': 6,
                'S10': 14,
                'S11': 95,
                '+FCLASS': 0,
                '+ICF': [3, 3],
                '+IFC': [2, 2],
                '+IPR': 115200,
                '+DR': 0,
                '+DS': [0, 0, 2048, 6],
                '+WS46': 12,
                '+CBST': [0, 0, 1],
            },
        )

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT&D1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_dtr(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_dtr(
            dtr=1,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT&S1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_dsr(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_dsr(
            always_on=True,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATV1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_result_format(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_result_format(
            verbose=True,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT&F\r', b'\r\nOK\r\n')], indirect=True)
    def test_reset_config(self, mock_v25ter_controller):
        result = mock_v25ter_controller.reset_config()

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATQ0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_result_presentation(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_result_presentation(
            transmit=True,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATX1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_connect_format(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_connect_format(
            mode=1,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT\\V0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_connect_protocol(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_connect_protocol(
            report=False,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT&E0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_connect_speed(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_connect_speed(
            report_serial=False,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT&W0\r', b'\r\nOK\r\n')], indirect=True)
    def test_save_config(self, mock_v25ter_controller):
        result = mock_v25ter_controller.save_config()

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'ATZ0\r', b'\r\nOK\r\n')], indirect=True)
    def test_restore_config(self, mock_v25ter_controller):
        result = mock_v25ter_controller.restore_config()

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CGMI\r', b'\r\nSIMCOM INCORPORATED\r\nOK\r\n')], indirect=True)
    def test_get_manufacturer(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_manufacturer()

        assert result == 'SIMCOM INCORPORATED'

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CGMM\r', b'\r\nSIMCOM_SIM7600C\r\nOK\r\n')], indirect=True)
    def test_get_model(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_model()

        assert result == 'SIMCOM_SIM7600C'

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CGMR\r', b'\r\n+CGMR: LE11B01SIM7600C\r\nOK\r\n')], indirect=True)
    def test_get_revision(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_revision()

        assert result == 'LE11B01SIM7600C'

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CGSN\r', b'\r\n351602000330570\r\nOK\r\n')], indirect=True)
    def test_get_serial(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_serial()

        assert result == 351602000330570

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CSCS="IRA"\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_te_charset(self, mock_v25ter_controller):
        result = mock_v25ter_controller.set_te_charset(
            char_set=enums.TECharacterSet.IRA,
        )

        assert result

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CSCS?\r', b'\r\n+CSCS: "IRA"\r\nOK\r\n')], indirect=True)
    def test_get_te_charset(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_te_charset()

        assert result == enums.TECharacterSet.IRA

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CIMI\r', b'\r\n460010222028133\r\nOK\r\n')], indirect=True)
    def test_get_international_subscriber(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_international_subscriber()

        assert result == 460010222028133

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+CIMIM\r', b'\r\n460010222028133\r\nOK\r\n')], indirect=True)
    def test_get_another_subscriber(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_another_subscriber()

        assert result == 460010222028133

    @pytest.mark.parametrize('mock_v25ter_controller', [(b'AT+GCAP\r', b'\r\n+GCAP:+CGSM,+FCLASS,+DS\r\nOK\r\n')], indirect=True)
    def test_get_capabilities(self, mock_v25ter_controller):
        result = mock_v25ter_controller.get_capabilities()

        assert_equal(
            result,
            {
                'CGSM': True,
                'FCLASS': True,
                'DS': True,
                'ES': False,
                'CIS707-A': False,
                'CIS-856': False,
                'MS': False,
            }
        )
