"""
This file contains classes related to status control commands.

This file may raise StatusControlException,
remember to capture accordingly.
"""

import re
from datetime import datetime, timedelta, timezone

from py_sim7600.controller import DeviceController
from py_sim7600.exceptions import StatusControlException, DeviceException
from py_sim7600.model import enums, sim_me
from py_sim7600.model.signal_quality import SignalQuality


class StatusController(DeviceController):
    """
    Controller for AT Commands for Status Control
    """

    def set_function(self,
                     function=enums.PhoneFunctionalityLevel.FULL,
                     reset=False,
                     ) -> bool:
        """
        Set phone functionality

        Corresponding command: AT+CFUN

        :param reset: Controls whether to reset the memory
        :param function: The function level to set the modem into
        :return: Results from device return buffer
        :rtype: bool
        :raises StatusControlException: Reset or restart required
        """

        command = 'AT+CFUN='

        status = self.get_function()

        if function != enums.PhoneFunctionalityLevel.OFFLINE \
                and function != enums.PhoneFunctionalityLevel.RESET \
                and status == enums.PhoneFunctionalityLevel.OFFLINE:
            # Restart required
            raise StatusControlException('Reset or restart required')

        command += str(function.value)

        if reset:
            command += ',1'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting function') from e

        return True

    def get_function(self) -> enums.PhoneFunctionalityLevel:
        """
        Get phone functionality

        Corresponding command: AT+CFUN?

        :return: Function level
        :rtype: enums.PhoneFunctionalityLevel
        """

        try:
            result = self.device.send(
                command='AT+CFUN?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting function') from e

        pattern = r'\+CFUN: (\d)'
        match = re.search(pattern, result)

        return enums.PhoneFunctionalityLevel(int(match.group(1)))

    def enter_pin(self, pin: str, puk: str = None) -> bool:
        """
        Enter PIN

        If this is a new SIM card, then the new PIN might be necessary.
        It will replace the current PIN.

        Corresponding command: AT+CPIN

        :param pin: The PIN of the SIM card.
        :param puk: The PUK of the SIM card.
        :return: True if successful
        :rtype: bool
        :raises StatusControlException: PUK required but not provided
        """

        command = 'AT+CPIN='

        # Check the current PIN request status
        try:
            result = self.device.send(
                command='AT+CPIN?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting PIN status') from e

        if 'READY' in result:
            # No PIN required
            raise StatusControlException('No PIN required')
        elif 'SIM PIN' in result or 'NET PIN' in result:
            # PIN, PIN2, PH PIN or NET PIN required
            command += pin
        elif 'SIM PUK' in result:
            # PUK or PUK2 required
            if not puk:
                raise StatusControlException('PUK required')
            else:
                command += puk + ',' + pin

        try:
            self.device.send(
                command=command,
                back="OK",
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error entering PIN') from e

        return True

    def get_iccid(self) -> str:
        """
        Read ICCID from SIM card

        Corresponding command: AT+CICCID

        :return: The ICCID of the SIM card
        :rtype: str
        """

        try:
            result = self.device.send(
                command='AT+CICCID',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting ICCID') from e

        pattern = r'\+ICCID: (\w+)'
        match = re.search(pattern, result)

        return match.group(1)

    def sim_access_general(self, command: sim_me.SIMMECommand) -> sim_me.SIMMEResponse:
        """
        Generic SIM access

        Corresponding command: AT+CSIM

        :param command: Command passed from MT to SIM card
        :return: SIM-ME response
        :rtype: sim_me.SIMMEResponse
        """

        apdu = command.apdu
        apdu_length = len(apdu)

        at_command = f'AT+CSIM={apdu_length},{apdu}'

        try:
            result = self.device.send(
                command=at_command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error sending APDU') from e

        response_apdu_pattern = r'\+CSIM: (\d+),"(.+)"'
        response_apdu = re.search(response_apdu_pattern, result).group(2)

        return sim_me.SIMMEResponse.parse(
            command_type=command.command_type,
            response=response_apdu
        )

    def sim_access_restricted(self,
                              command: enums.RestrictedSIMCommand,
                              file_id: enums.ElementaryFileID = None,
                              p1: int = None,
                              p2: int = None,
                              p3: int = None,
                              data: str = None,
                              ) -> sim_me.SIMMEResponse:
        """
        Restricted SIM access

        Corresponding command: AT+CRSM

        :param command: Command passed on by the MT to the SIM
        :param file_id: Identifier for an elementary data file on SIM, if used by the command
        :param p1: First parameter for the command
        :param p2: Second parameter for the command
        :param p3: Third parameter for the command
        :param data: Data to be written to the SIM
        :return: SIM-ME response
        :rtype: sim_me.SIMMEResponse
        """

        command_out = 'AT+CRSM=' + str(command.value)

        if file_id is not None:
            command_out += ',' + str(file_id.value)
        if p1 is not None:
            command_out += ',' + str(p1)
        if p2 is not None:
            command_out += ',' + str(p2)
        if p3 is not None:
            command_out += ',' + str(p3)
        if data is not None:
            # Data needs to be in hexadecimal format
            try:
                assert len(data) % 2 == 0
                assert all(c in '0123456789ABCDEF' for c in data)
            except AssertionError:
                raise StatusControlException('Data must be in hexadecimal format')

            command_out += ',' + data

        try:
            result = self.device.send(
                command=command_out,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error sending restricted SIM command') from e

        return sim_me.SIMMEResponse.parse(
            command_type=command.to_sim_me(),
            response=result
        )

    def pin_times(self) -> tuple[int, int, int, int]:
        """
        Times remain to input SIM PIN/PUK

        Corresponding command: AT+SPIC

        :return: The remaining times to input PIN1, PUK1, PIN2, PUK2 as a tuple
        """

        try:
            result = self.device.send(
                command='AT+SPIC',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error reading remaining PIN input times') from e

        pattern = r'\+SPIC: (\d+),(\d+),(\d+),(\d+)'
        match = re.search(pattern, result)

        return (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4))
        )

    def get_provider(self) -> tuple[str, bool]:
        """
        Get service provider name from SIM

        Corresponding command: AT+CSPN

        :return: Provider name and whether the PLMN is displayed, in a tuple
        :rtype: tuple
        """

        try:
            result = self.device.send(
                command='AT+CSPN?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting service provider name') from e

        pattern = r'\+CSPN: "(\w+)",(\d)'
        match = re.search(pattern, result)

        return match.group(1), bool(int(match.group(2)))

    def get_signal(self) -> SignalQuality:
        """
        Query signal quality

        Corresponding command: AT+CSQ

        :return: A SignalQuality object representing the signal quality
        :rtype: SignalQuality
        """

        try:
            result = self.device.send(
                command='AT+CSQ',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting signal quality') from e

        pattern = r'\+CSQ: \d+,\d+'
        match = re.search(pattern, result)

        if match:
            return SignalQuality.from_quality_query(match.group())

        raise StatusControlException('Invalid response')

    def set_auto_csq(self, auto_report=False, when_changed=False) -> bool:
        """
        Set CSQ report

        Corresponding command: AT+AUTOCSQ

        :param auto_report: Whether to automatically report CSQ
        :param when_changed: Whether to report when CSQ changes, or every 5 seconds
        :return: True if successful
        :rtype: bool
        """

        command = f'AT+AUTOCSQ={int(auto_report)},{int(when_changed)}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting CSQ report') from e

        return True

    def get_auto_csq(self) -> tuple[bool, bool]:
        """
        Get CSQ report settings

        Corresponding command: AT+AUTOCSQ?

        :return: Whether to automatically report CSQ and whether to report when CSQ changes
        :rtype: tuple
        """

        try:
            result = self.device.send(
                command='AT+AUTOCSQ?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting CSQ report settings') from e

        pattern = r'\+AUTOCSQ: (\d),(\d)'
        match = re.search(pattern, result)

        return bool(int(match.group(1))), bool(int(match.group(2)))

    def set_rssi(self, delta=5) -> bool:
        """
        Set RSSI delta change threshold

        Corresponding command: AT+CSQDELTA

        :return: True if successful
        :rtype: bool
        :raises StatusControlException: Delta value error
        """

        if delta < 0 or delta > 5:
            raise StatusControlException('Delta value error')

        try:
            self.device.send(
                command=f'AT+CSQDELTA={delta}',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting RSSI delta') from e

        return True

    def get_rssi(self) -> int:
        """
        Get RSSI delta change threshold

        Corresponding command: AT+CSQDELTA?

        :return: RSSI delta change threshold
        :rtype: int
        """

        try:
            result = self.device.send(
                command='AT+CSQDELTA?',
                back='OK',
            )
        except DeviceException as e:
            raise StatusControlException('Error getting RSSI delta') from e

        pattern = r'\+CSQDELTA: (\d)'
        match = re.search(pattern, result)

        return int(match.group(1))

    def set_urc(self, port=enums.URCPort.ALL) -> bool:
        """
        Configure URC destination interface

        Corresponding command: AT+CATR

        :param port: The URC destination interface
        :return: True if successful
        :rtype: bool
        """

        try:
            self.device.send(
                command=f'AT+CATR={port.value}',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting URC port') from e

        return True

    def get_urc(self) -> enums.URCPort:
        """
        Get URC destination interface

        Corresponding command: AT+CATR?

        :return: URC destination interface
        :rtype: enums.URCPort
        """

        try:
            result = self.device.send(
                command='AT+CATR?',
                back='OK',
            )
        except DeviceException as e:
            raise StatusControlException('Error getting URC port') from e

        pattern = r'\+CATR: (\d)'
        match = re.search(pattern, result)

        return enums.URCPort(int(match.group(1)))

    def power_down(self) -> bool:
        """
        Power down the module

        Corresponding command: AT+CPOF

        :return: True if successful
        :rtype: bool
        """

        try:
            self.device.send(
                command='AT+CPOF',
                back='OK',
            )
        except DeviceException as e:
            raise StatusControlException('Error powering down') from e

        return True

    def reset(self) -> bool:
        """
        Reset the module

        Corresponding command: AT+CRESET

        :return: True if successful
        :rtype: bool
        """

        try:
            self.device.send(
                command='AT+CRESET',
                back='OK',
            )
        except DeviceException as e:
            raise StatusControlException('Error resetting') from e

        return True

    def reset_accumulated_meter(self, pin: str) -> bool:
        """
        Reset the accumulated call meter

        Corresponding command: AT+CACM

        :param pin: The password to reset the meter, usually PIN2
        :return: True if successful
        :rtype: bool
        """

        command = f'AT+CACM="{pin}"'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error resetting accumulated meter') from e

        return True

    def get_accumulated_meter(self) -> int:
        """
        Get the accumulated call meter value

        Corresponding command: AT+CACM?

        :return: The accumulated call meter
        :rtype: int
        """

        try:
            result = self.device.send(
                command='AT+CACM?',
                back='OK',
            )
        except DeviceException as e:
            raise StatusControlException('Error getting accumulated meter') from e

        pattern = r'\+CACM: "(\d{2})(\d{2})(\d{2})"'
        match = re.search(pattern, result)

        accumulated_time = int(match.group(3)) + int(match.group(2)) * 60 + int(match.group(1)) * 3600

        return accumulated_time

    def set_acm_maximum(self, max_sec: int, pin: str = None) -> bool:
        """
        Set the accumulated call meter maximum time

        Corresponding command: AT+CAMM

        :param max_sec: The maximum time in seconds; 0 to disable
        :param pin: The password to set the maximum, usually PIN2
        :return: True if successful
        :rtype: bool
        """

        acm_value = (str(max_sec // 3600).zfill(2) +
                     str((max_sec % 3600) // 60).zfill(2) +
                     str((max_sec % 3600) % 60).zfill(2))
        
        command = f'AT+CAMM="{acm_value}"'

        if pin is not None:
            command += f',"{pin}"'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting ACM maximum') from e

        return True

    def get_acm_maximum(self) -> int:
        """
        Get the accumulated call meter maximum time

        Corresponding command: AT+CAMM?

        :return: The maximum time in seconds
        :rtype: int
        """

        try:
            result = self.device.send(
                command='AT+CAMM?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting ACM maximum') from e

        pattern = r'\+CAMM: "(\d{2})(\d{2})(\d{2})"'
        match = re.search(pattern, result)

        max_time = int(match.group(3)) + int(match.group(2)) * 60 + int(match.group(1)) * 3600

        return max_time

    def set_price_per_unit(self, currency: str, ppu: float, pin: str = None) -> bool:
        """
        Price per unit and currency table

        Corresponding command: AT+CPUC

        :param currency: The currency code, 3-letter code as per ISO 4217
        :param ppu: The price per unit
        :param pin: The password to set the price per unit, usually PIN2
        :return: True if successful
        :rtype: bool
        """

        command = f'AT+CPUC="{currency}","{ppu:.2f}"'

        if pin is not None:
            command += f',"{pin}"'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting price per unit') from e

        return True

    def get_price_per_unit(self) -> tuple[str, float]:
        """
        Get the price per unit and currency

        Corresponding command: AT+CPUC?

        :return: The currency code and price per unit
        :rtype: tuple
        """

        try:
            result = self.device.send(
                command='AT+CPUC?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting price per unit') from e

        pattern = r'\+CPUC: "(\w+)","([\d.]+)"'
        match = re.search(pattern, result)

        return match.group(1), float(match.group(2))

    def set_rtc(self, time: datetime) -> bool:
        """
        Real time clock management

        Corresponding command: AT+CCLK

        :param time: The time to set the RTC to
        :return: True if successful
        :rtype: bool
        """

        time_str = time.strftime('%y/%m/%d,%H:%M:%S')
        offset = int(time.utcoffset().total_seconds() // 60 // 15)
        if offset >= 0:
            time_str += f'+{offset:02d}'
        else:
            time_str += f'-{-offset:02d}'
        
        command = f'AT+CCLK="{time_str}"'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting RTC') from e

        return True

    def get_rtc(self) -> datetime:
        """
        Get the real time clock

        Corresponding command: AT+CCLK?

        :return: The real time clock
        :rtype: datetime
        """

        try:
            result = self.device.send(
                command='AT+CCLK?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting RTC') from e

        pattern = r'\+CCLK: "(\d{2}/\d{2}/\d{2},\d{2}:\d{2}:\d{2})([+-]\d{2})?"'
        match = re.search(pattern, result)

        time = datetime.strptime(match.group(1), '%y/%m/%d,%H:%M:%S')
        tz = match.group(2)
        if tz:
            offset = timedelta(minutes=int(tz) * 15)

            time = time.replace(tzinfo=timezone(offset))

        return time

    def set_error_report(self, report_mode=enums.MEErrorReportMode.VERBOSE) -> bool:
        """
        Report mobile equipment error

        Corresponding command: AT+CMEE

        :param report_mode: The error report mode
        :return: True if successful
        """

        command = f'AT+CMEE={report_mode.value}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting error report') from e

        return True

    def get_error_report(self) -> enums.MEErrorReportMode:
        """
        Get mobile equipment error report mode

        Corresponding command: AT+CMEE?

        :return: The error report mode
        :rtype: enums.MEErrorReportMode
        """

        try:
            result = self.device.send(
                command='AT+CMEE?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting error report') from e

        pattern = r'\+CMEE: (\d)'
        match = re.search(pattern, result)

        return enums.MEErrorReportMode(int(match.group(1)))

    def get_activity(self) -> enums.PhoneActivityStatus:
        """
        Phone activity status

        Corresponding command: AT+CPAS

        :return: The phone activity status
        :rtype: enums.PhoneActivityStatus
        """

        try:
            result = self.device.send(
                command='AT+CPAS',
                back='OK',
            )
        except DeviceException as e:
            raise StatusControlException('Error getting activity') from e

        pattern = r'\+CPAS: (\d)'
        match = re.search(pattern, result)
        status = enums.PhoneActivityStatus(int(match.group(1)))

        return status

    def set_imei(self, imei: int) -> bool:
        """
        Set IMEI for the module

        Corresponding command: AT+SIMEI

        :param imei: The IMEI to set
        :return: True if successful
        :rtype: bool
        """

        command = f'AT+SIMEI={imei:015d}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting IMEI') from e

        return True

    def get_imei(self) -> int:
        """
        Get IMEI of the module

        Corresponding command: AT+SIMEI?

        :return: The IMEI of the module
        :rtype: int
        """

        try:
            result = self.device.send(
                command='AT+SIMEI?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting IMEI') from e

        pattern = r'\+SIMEI: (\d{15})'
        match = re.search(pattern, result)

        return int(match.group(1))

    def get_equipment_id(self) -> str:
        """
        Request Mobile Equipment Identifier

        Corresponding command: AT+SMEID

        :param device: A SIM7600 device instance
        :return: The equipment ID
        :rtype: str
        """

        try:
            result = self.device.send(
                command="AT+SMEID?",
                back="OK"
            )
        except DeviceException as e:
            raise StatusControlException('Error getting equipment ID') from e

        pattern = r'\+SMEID: (\w+)'
        match = re.search(pattern, result)

        return match.group(1)

    def set_voicemail_number(self, number: str, valid: bool, number_type: enums.CallNumberType) -> bool:
        """
        Set voice Mail Subscriber number

        Corresponding command: AT+CSVM

        :return: True if successful
        :raises StatusControlException: Invalid number or number type
        """

        pattern = r'[\d\+]*'
        if not re.match(pattern, number):
            raise StatusControlException('Invalid number')

        if number_type not in [
            enums.CallNumberType.RESTRICTED,
            enums.CallNumberType.INTERNATIONAL,
            enums.CallNumberType.OTHER,
        ]:
            raise StatusControlException('Invalid number type')
        
        command = f'AT+CSVM={int(valid)},"{number}",{number_type.value}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error setting voicemail number') from e

        return True

    def get_voicemail_number(self) -> tuple[bool, str, enums.CallNumberType]:
        """
        Get voice Mail Subscriber number

        Corresponding command: AT+CSVM?

        :return: The voicemail number, whether it is valid, and the number type
        :rtype: tuple
        """

        try:
            result = self.device.send(
                command='AT+CSVM?',
                back='OK',
                error_pattern=['ERROR'],
            )
        except DeviceException as e:
            raise StatusControlException('Error getting voicemail number') from e

        pattern = r'\+CSVM: (\d),"([\d\+]+)",(\d+)'
        match = re.search(pattern, result)

        return bool(int(match.group(1))), match.group(2), enums.CallNumberType(int(match.group(3)))
