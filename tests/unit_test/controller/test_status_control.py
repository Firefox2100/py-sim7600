import pytest
from datetime import datetime
from pytz import timezone
from numpy.testing import assert_equal

from py_sim7600.controller.status_control import StatusController, StatusControlException
from py_sim7600.model import enums
from py_sim7600.model.signal_quality import SignalQuality


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
    @pytest.mark.parametrize('mock_status_controller', [(b'AT"\r', b'\r\nOK\r\n')], indirect=True)
    def test_command_with_timeout(self, mock_status_controller):
        """
        Test the timeout for a command by sending a command that will not be responded to.

        It's at the beginning to allow pytest-xdist to run this one first.
        """
        with pytest.raises(StatusControlException):
            mock_status_controller.set_function(enums.PhoneFunctionalityLevel.MINIMUM)

        with pytest.raises(StatusControlException):
            mock_status_controller.get_function()

        with pytest.raises(StatusControlException):
            mock_status_controller.enter_pin('123456')

        with pytest.raises(StatusControlException):
            mock_status_controller.get_iccid()

        with pytest.raises(StatusControlException):
            mock_status_controller.pin_times()

        with pytest.raises(StatusControlException):
            mock_status_controller.get_provider()

        with pytest.raises(StatusControlException):
            mock_status_controller.get_signal()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_auto_csq(
                auto_report=True,
                when_changed=True,
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_auto_csq()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_rssi(
                delta=3,
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_rssi()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_urc(
                port=enums.URCPort.UART,
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_urc()

        with pytest.raises(StatusControlException):
            mock_status_controller.power_down()

        with pytest.raises(StatusControlException):
            mock_status_controller.reset()

        with pytest.raises(StatusControlException):
            mock_status_controller.reset_accumulated_meter(
                pin='123456',
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_accumulated_meter()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_acm_maximum(
                max_sec=3600,
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_acm_maximum()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_price_per_unit(
                currency='GBP',
                ppu=2.66,
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_price_per_unit()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_rtc(
                time=datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone('UTC')),
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_rtc()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_error_report(
                report_mode=enums.MEErrorReportMode.DISABLE,
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_error_report()

        with pytest.raises(StatusControlException):
            mock_status_controller.get_activity()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_imei(
                imei=357396012183170,
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_imei()

        with pytest.raises(StatusControlException):
            mock_status_controller.get_equipment_id()

        with pytest.raises(StatusControlException):
            mock_status_controller.set_voicemail_number(
                valid=True,
                number='13697252277',
                number_type=enums.CallNumberType.OTHER
            )

        with pytest.raises(StatusControlException):
            mock_status_controller.get_voicemail_number()

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

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CSQ\r', b'\r\n+CSQ: 22,0\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_signal(self, mock_status_controller):
        result = mock_status_controller.get_signal()

        assert result == SignalQuality(
            strength=-69,
            is_rscp=False,
            bit_error_rate=0,
        )

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+AUTOCSQ=1,1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_auto_csq(self, mock_status_controller):
        result = mock_status_controller.set_auto_csq(
            auto_report=True,
            when_changed=True,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+AUTOCSQ?\r', b'\r\n+AUTOCSQ: 1,1\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_auto_csq(self, mock_status_controller):
        result = mock_status_controller.get_auto_csq()

        assert result

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CSQDELTA=3\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_rssi(self, mock_status_controller):
        result = mock_status_controller.set_rssi(
            delta=3,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CSQDELTA?\r', b'\r\n+CSQDELTA: 3\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_rssi(self, mock_status_controller):
        result = mock_status_controller.get_rssi()

        assert result == 3

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CATR=1\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_urc(self, mock_status_controller):
        result = mock_status_controller.set_urc(
            port=enums.URCPort.UART,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CATR?\r', b'\r\n+CATR: 1\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_urc(self, mock_status_controller):
        result = mock_status_controller.get_urc()

        assert result == enums.URCPort.UART

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CPOF\r', b'\r\nOK\r\n')], indirect=True)
    def test_power_down(self, mock_status_controller):
        result = mock_status_controller.power_down()

        assert result

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CRESET\r', b'\r\nOK\r\n')], indirect=True)
    def test_reset(self, mock_status_controller):
        result = mock_status_controller.reset()

        assert result

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CACM="123456"\r', b'\r\nOK\r\n')], indirect=True)
    def test_reset_accumulated_meter(self, mock_status_controller):
        result = mock_status_controller.reset_accumulated_meter(
            pin='123456',
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CACM?\r', b'\r\n+CACM: "010203"\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_accumulated_meter(self, mock_status_controller):
        result = mock_status_controller.get_accumulated_meter()

        assert result == 3723

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CAMM="010000"\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_acm_maximum(self, mock_status_controller):
        result = mock_status_controller.set_acm_maximum(
            max_sec=3600,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CAMM?\r', b'\r\n+CAMM: "010000"\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_acm_maximum(self, mock_status_controller):
        result = mock_status_controller.get_acm_maximum()

        assert result == 3600

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CPUC="GBP","2.66"\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_price_per_unit(self, mock_status_controller):
        result = mock_status_controller.set_price_per_unit(
            currency='GBP',
            ppu=2.66,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CPUC?\r', b'\r\n+CPUC: "GBP","2.66"\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_price_per_unit(self, mock_status_controller):
        result = mock_status_controller.get_price_per_unit()

        assert_equal(result, ('GBP', 2.66))

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CCLK="21/01/01,00:00:00+00"\r', b'\r\nOK\r\n')],
        indirect=True,
    )
    def test_set_rtc(self, mock_status_controller):
        time = datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone('UTC'))

        result = mock_status_controller.set_rtc(
            time=time,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CCLK?\r', b'\r\n+CCLK: "21/01/01,00:00:00+00"\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_rtc(self, mock_status_controller):
        result = mock_status_controller.get_rtc()

        assert result == datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone('UTC'))

    @pytest.mark.parametrize('mock_status_controller', [(b'AT+CMEE=0\r', b'\r\nOK\r\n')], indirect=True)
    def test_set_error_report(self, mock_status_controller):
        result = mock_status_controller.set_error_report(
            report_mode=enums.MEErrorReportMode.DISABLE,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CMEE?\r', b'\r\n+CMEE: 2\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_error_report(self, mock_status_controller):
        result = mock_status_controller.get_error_report()

        assert result == enums.MEErrorReportMode.VERBOSE

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CPAS\r', b'\r\n+CPAS: 3\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_activity(self, mock_status_controller):
        result = mock_status_controller.get_activity()

        assert result == enums.PhoneActivityStatus.RINGING

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+SIMEI=357396012183170\r', b'\r\nOK\r\n')],
        indirect=True,
    )
    def test_set_imei(self, mock_status_controller):
        result = mock_status_controller.set_imei(
            imei=357396012183170,
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+SIMEI?\r', b'\r\n+SIMEI: 357396012183170\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_imei(self, mock_status_controller):
        result = mock_status_controller.get_imei()

        assert result == 357396012183170

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+SMEID?\r', b'\r\n+SMEID: A1000021A5906F\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_equipment_id(self, mock_status_controller):
        result = mock_status_controller.get_equipment_id()

        assert result == 'A1000021A5906F'

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CSVM=1,"13697252277",129\r', b'\r\nOK\r\n')],
        indirect=True,
    )
    def test_set_voicemail_number(self, mock_status_controller):
        result = mock_status_controller.set_voicemail_number(
            valid=True,
            number='13697252277',
            number_type=enums.CallNumberType.OTHER
        )

        assert result

    @pytest.mark.parametrize(
        'mock_status_controller',
        [(b'AT+CSVM?\r', b'\r\n+CSVM: 1,"13697252277",129\r\nOK\r\n')],
        indirect=True,
    )
    def test_get_voicemail_number(self, mock_status_controller):
        result = mock_status_controller.get_voicemail_number()

        assert result == (True, '13697252277', enums.CallNumberType.OTHER)
