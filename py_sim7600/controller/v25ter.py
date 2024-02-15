"""
This file contains classes related to V.25TER commands.

This file may raise V25TERException,
remember to capture accordingly.
"""

import time
import re

from py_sim7600.controller import DeviceController
from py_sim7600.exceptions import V25TERException, DeviceException
from py_sim7600.model import enums


class V25TERController(DeviceController):
    """
    Controller for AT Commands According to V.25TER
    """

    def re_issue(self) -> str:
        """
        Re-issues the Last Command Given

        Corresponding command: A/

        :return: Results of the last command
        :rtype: str
        """

        result = self.device.send(
            command='A/',
        )

        return result

    def dial(self, number: str, anonymous=False, cug_invocation=False, voice=True) -> bool:
        """
        Mobile Originated Call to Dial A Number

        Corresponding command: ATD

        :param voice: Control whether to make a data call
        :param cug_invocation: Control whether this call should invoke Closed User Group
        :param anonymous: Control whether to display caller number
        :param number: Number to call
        :return: True if call is successful
        :rtype: bool
        """

        command = 'ATD' + number
        back = 'OK'
        if anonymous:
            command += 'I'

        if cug_invocation:
            command += 'G'

        if voice:
            command += ';'
        else:
            back = 'CONNECT'

        self.device.send(
            command=command,
            back=back,
        )

        return True

    def dial_from(self, target: str | int, memory: enums.PhonebookStorage = None, voice=True) -> bool:
        """
        Originate call from specified memory or active memory

        Corresponding command: ATD>

        :param voice: Control whether to make a data call
        :param memory: The memory to pull number from. Leave empty to use currently active memory
        :param target: The target to call
        :return: True if call is successful
        :rtype: bool
        :raises AssertionError: Memory type error
        """

        command = 'ATD>'
        back = 'OK'

        if isinstance(target, str):
            target = f'"{target}"'
        elif isinstance(target, int):
            target = str(target)
        else:
            raise TypeError('Target type error')

        if memory is None:
            # From active memory
            command += target
        else:
            command += memory.value + target

        if voice:
            command += ';'
        else:
            back = 'CONNECT'

        self.device.send(
            command=command,
            back=back,
        )

        return True

    def answer(self) -> bool:
        """
        Call answer

        Corresponding command: ATA

        :return: True if answering call is successful
        :rtype: bool
        :raises V25TERException: No incoming call
        """

        try:
            result = self.device.send(
                command='ATA',
                back='OK',
            )

            if 'NO CARRIER' in result:
                raise V25TERException("No incoming call or no reception")
        except DeviceException as e:
            raise V25TERException from e

        return True

    def disconnect(self) -> bool:
        """
        Disconnect existing call

        Corresponding command: ATH

        :return: True if call is disconnected
        :rtype: bool
        """

        from .call_control import CallController

        call_controller = CallController(self.device)

        try:
            call_controller.set_control_voice_hangup(disconnect_ath=True)
        except Exception as e:
            if not call_controller.check_control_voice_hangup():
                raise e

        self.device.send(
            command='ATH',
            back='OK'
        )

        return True

    def set_auto_answer(self, times: int) -> bool:
        """
        Automatic answer incoming call

        Corresponding command: ATS0

        :param times: Times of ring to auto answer. Set to 0 to disable auto answer.
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Auto answer time set to too long or too short
        """

        command = 'ATS0='

        if times > 255 or times < 0:
            raise V25TERException('Auto answer times out of range')

        command += str(times).zfill(3)

        self.device.send(
            command=command,
            back='OK',
        )

        return True

    def get_auto_answer(self) -> int:
        """
        Check the auto answer configuration

        Corresponding command: ATS0

        :return: Results from device return buffer
        :rtype: int
        :raises V25TERException: Auto answer time set to too long or too short
        """

        command = 'ATS0?'

        result = self.device.send(
            command=command,
            back='OK',
        )

        times = int(result[0:3])

        return times

    def switch_to_command(self) -> bool:
        """
        Switch from data mode to command mode

        Corresponding command: +++

        :return: True if switch is successful
        :rtype: bool
        """

        time.sleep(1)

        self.device.send(
            command='+++',
            back='OK',
        )

        return True

    def switch_to_data(self) -> bool:
        """
        Switch from command mode to data mode

        Corresponding command: ATO

        :return: True if switch is successful
        :rtype: bool
        """

        self.device.send(
            command='ATO',
            back='CONNECT',
        )

        return True

    def info(self) -> dict:
        """
        Display product identification information

        Corresponding command: ATI

        :return: Identification information
        :rtype: dict
        """

        result = self.device.send(
            command='ATI',
            back='OK',
        )

        result_dict = {}

        for line in result.split('\r'):
            if line != 'OK':
                key, value = line.split(': ')

                if ',' in value:
                    value = value.split(',')

                if key == 'Manufacturer':
                    result_dict['manufacturer'] = value
                elif key == 'Model':
                    result_dict['model'] = value
                elif key == 'Revision':
                    result_dict['revision'] = value
                elif key == 'IMEI':
                    result_dict['imei'] = int(value)
                elif key == '+GCAP':
                    result_dict['capabilities'] = []
                    for v in value:
                        result_dict['capabilities'].append(v.strip('+'))

        return result_dict

    def set_baud(self, baud: int) -> bool:
        """
        Set local baud rate temporarily

        Corresponding command: AT+IPR

        :param baud: The baud rate to set.
        :return: True if setting is successful
        :rtype: bool
        """

        command = 'AT+IPR=' + str(baud)

        self.device.send(
            command=command,
            back='OK',
        )

        return True

    def get_baud(self) -> int:
        """
        Check the current baud rate setting

        Corresponding command: AT+IPR?

        :return: The current baud rate setting
        :rtype: int
        """

        result = self.device.send(
            command='AT+IPR?',
            back='OK',
        )

        pattern = r'\+IPR: (\d+)'
        result = re.search(pattern, result)

        return int(result.group(1))

    def set_control_character(self,
                              format_control: enums.ControlCharacterFormat,
                              parity: enums.ControlCharacterParity = None,
                              ) -> bool:
        """
        Set control character framing

        Corresponding command: AT+ICF

        :param parity: Parity bit format
        :param format_control: Control format
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Parity code error or Format code error
        """

        command = 'AT+ICF='

        if format_control == enums.ControlCharacterFormat.D7P1S1 or \
                format_control == enums.ControlCharacterFormat.D8P1S1:
            if parity is None:
                raise V25TERException('Parity code need to be set for this format')
            else:
                command += f'{format_control.value},{parity.value}'
        else:
            if parity is not None and parity != enums.ControlCharacterParity.NONE:
                raise V25TERException('Parity code no need to be set for this format')
            else:
                command += str(format_control.value)

        result = self.device.send(
            command=command,
            back='OK',
        )

        return result

    def get_control_character(self) -> (enums.ControlCharacterFormat, enums.ControlCharacterParity):
        """
        Check the current control character framing setting

        Corresponding command: AT+ICF?

        :return: The current control character framing setting
        :rtype: tuple
        """

        result = self.device.send(
            command='AT+ICF?',
            back='OK',
        )

        pattern = r'\+ICF: (\d+),(\d+)'
        result = re.search(pattern, result)

        return (
            enums.ControlCharacterFormat(int(result.group(1))),
            enums.ControlCharacterParity(int(result.group(2)))
        )

    def set_data_flow(self, rts=False, cts=False) -> bool:
        """
        Set local data flow control

        Corresponding command: AT+IFC

        :param rts: Whether to set RTS hardware flow control
        :param cts: Whether to set CTS hardware flow control
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Control value error
        """

        command = 'AT+IFC='

        dce = 2 if rts else 0
        dte = 2 if cts else 0

        command += f'{dce},{dte}'

        self.device.send(
            command=command,
            back='OK',
        )

        return True

    def get_data_flow(self) -> (bool, bool):
        """
        Check the current data flow control setting

        Corresponding command: AT+IFC?

        :return: The current data flow control setting
        :rtype: tuple
        """

        result = self.device.send(
            command='AT+IFC?',
            back='OK',
        )

        pattern = r'\+IFC: (\d+),(\d+)'
        result = re.search(pattern, result)

        return (
            int(result.group(1)) == 2,
            int(result.group(2)) == 2
        )

    def set_dcd_function(self, dcd: int) -> bool:
        """
        Set DCD function mode

        Corresponding command: AT&C

        :param dcd: The DCD setting to be set
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: DCD value error
        """

        if dcd < 0 or dcd > 2:
            raise V25TERException('DCD value error')

        self.device.send(
            command='AT&C' + str(dcd),
            back='OK',
        )

        return True

    def enable_command_echo(self, enable: bool) -> bool:
        """
        Enable command echo

        Corresponding command: ATE

        :param enable: Controls whether the command echo should be enabled
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Device echo value error
        """

        self.device.send(
            command='ATE' + str(int(enable)),
            back='OK',
        )

        return True

    def current_config(self) -> dict:
        """
        Display current configuration

        Corresponding command: AT&V

        :return: Configurations returned by the device
        :rtype: dict
        """

        result = self.device.send(
            command='AT&V',
            back='OK',
        )

        config = {}
        items = result.split('\r')

        for item in items:
            item = item.strip()
            if not item:
                continue

            config_set = item.split(';')
            for c in config_set:
                c = c.strip()
                if not c or c == 'OK':
                    continue

                k, v = c.split(':')
                k = k.strip()
                v = v.strip()

                if ',' in v:
                    v = v.split(',')

                    for i in range(len(v)):
                        try:
                            v[i] = int(v[i])
                        except ValueError:
                            pass
                else:
                    try:
                        v = int(v)
                    except ValueError:
                        pass

                config[k] = v

        return config

    def set_dtr(self, dtr: int):
        """
        Set DTR function mode

        Corresponding command: AT&D

        :param dtr: The mode to set DTR PIN function behaviour
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: DTR Mode value error
        """

        if dtr < 0 or dtr > 2:
            raise V25TERException('DTR Mode value error')

        self.device.send(
            command='AT&D' + str(dtr),
            back='OK',
        )

        return True

    def set_dsr(self, always_on: bool) -> bool:
        """
        Set DSR function mode

        Corresponding command: AT&S

        :param always_on: Set whether DSR is always on
        :return: True if setting is successful
        :rtype: bool
        """

        self.device.send(
            command='AT&S' + str(int(always_on)),
            back='OK',
        )

        return True

    def set_result_format(self, verbose: bool) -> bool:
        """
        Set result code format mode

        Corresponding command: ATV

        :param verbose: Set whether to use long, verbose format
        :return: True if setting is successful
        :rtype: bool
        """

        self.device.send(
            command='ATV' + str(int(verbose)),
            back='OK',
        )

        return True

    def reset_config(self, temporary=False) -> bool:
        """
        Set all current parameters to manufacturer defaults

        Corresponding command: AT&F

        :param temporary: Set some temporary TA parameters to manufacturer defaults
        :return: True if setting is successful
        :rtype: bool
        """

        command = 'AT&F'

        if temporary:
            command += '0'

        self.device.send(
            command=command,
            back='OK',
        )

        return True

    def set_result_presentation(self, transmit=True) -> bool:
        """
        Set Result Code Presentation Mode

        Corresponding command: ATQ

        :param transmit: Set whether DCE transmits result code
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Result format display mode value error
        """

        if transmit:
            dce = 0
        else:
            dce = 1

        self.device.send(
            command='ATQ' + str(dce),
            back='OK',
        )

        return True

    def set_connect_format(self, mode=1) -> bool:
        """
        Set CONNECT Result Code Format

        Corresponding command: ATX

        :param mode: Set whether CONNECT is returned
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Connect mode value error
        """

        if mode < 0 or mode > 4:
            raise V25TERException('Connect mode value error')

        self.device.send(
            command='ATX' + str(mode),
            back='OK',
        )

        return True

    def set_connect_protocol(self, report=False) -> bool:
        """
        Set CONNECT Result Code Format About Protocol

        Corresponding command: AT\\V

        :param report: Set whether to report communication protocol
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Report mode value error
        """

        self.device.send(
            command='AT\\V' + str(int(report)),
            back='OK',
        )

        return True

    def set_connect_speed(self, report_serial=True) -> bool:
        """
        Set CONNECT Result Code Format About Speed

        Corresponding command: AT&E

        :param report_serial: Set whether to report serial speed or wireless speed
        :return: True if setting is successful
        :rtype: bool
        """

        self.device.send(
            command='AT&E' + str(int(report_serial)),
            back='OK',
        )

        return True

    def save_config(self) -> bool:
        """
        Save the user setting to ME

        Corresponding command: AT&W

        :return: True if setting is successful
        :rtype: bool
        """

        self.device.send(
            command='AT&W0',
            back='OK',
        )

        return True

    def restore_config(self) -> bool:
        """
        Restore the user setting from ME

        Corresponding command: ATZ

        :return: True if setting is successful
        :rtype: bool
        """

        self.device.send(
            command='ATZ0',
            back='OK',
        )

        return True

    def get_manufacturer(self) -> str:
        """
        Request manufacturer identification

        Corresponding command: AT+CGMI

        :return: Manufacturer identification
        :rtype: str
        """

        result = self.device.send(
            command='AT+CGMI',
            back='OK',
        )

        return result.split('\r')[0]

    def get_model(self) -> str:
        """
        Request model identification

        Corresponding command: AT+CGMM

        :return: Model identification
        :rtype: str
        """

        result = self.device.send(
            command='AT+CGMM',
            back='OK',
        )

        return result.split('\r')[0]

    def get_revision(self) -> str:
        """
        Request revision identification

        Corresponding command: AT+CGMR

        :return: Revision identification
        :rtype: str
        """

        result = self.device.send(
            command='AT+CGMR',
            back='OK',
        )

        revision = result.split('\r')[0].split(' ')[1]

        return revision

    def get_serial(self) -> int:
        """
        Request product serial number identification

        Corresponding command: AT+CGSN

        :return: Serial number identification
        :rtype: int
        """

        result = self.device.send(
            command='AT+CGSN',
            back='OK',
        )

        return int(result.split('\r')[0])

    def set_te_charset(self, char_set: enums.TECharacterSet):
        """
        Select TE character set

        Corresponding command: AT+CSCS

        :param char_set: The character set to use
        :return: True if setting is successful
        :rtype: bool
        """

        command = 'AT+CSCS=' + f'"{char_set.value}"'

        self.device.send(
            command=command,
            back='OK',
        )

        return True

    def get_te_charset(self) -> enums.TECharacterSet:
        """
        Request TE character set

        Corresponding command: AT+CSCS?

        :return: The character set currently in use
        :rtype: enums.TECharacterSet
        """

        result = self.device.send(
            command='AT+CSCS?',
            back='OK',
        )

        pattern = r'\+CSCS: "(\w+)"'
        result = re.search(pattern, result)

        return enums.TECharacterSet(result.group(1))

    def get_international_subscriber(self) -> int:
        """
        Request international mobile subscriber identity

        Corresponding command: AT+CIMI

        :return: International mobile subscriber identity
        :rtype: int
        """

        result = self.device.send(
            command='AT+CIMI',
            back='OK',
        )

        pattern = r'(^\d{15})'
        result = re.search(pattern, result)

        return int(result.group(1))

    def get_another_subscriber(self) -> int:
        """
        Request another international mobile subscriber identity

        Corresponding command: AT+CIMIM

        :return: International mobile subscriber identity
        :rtype: int
        """

        result = self.device.send(
            command='AT+CIMIM',
            back='OK',
        )

        pattern = r'(^\d{15})'
        result = re.search(pattern, result)

        return int(result.group(1))

    def get_capabilities(self) -> dict:
        """
        Request overall capabilities

        Corresponding command: AT+GCAP

        :return: Capabilities
        :rtype: dict
        """

        result = self.device.send(
            command='AT+GCAP',
            back='OK',
        )

        capabilities = {
            'CGSM': '+CGSM' in result,
            'FCLASS': '+FCLASS' in result,
            'DS': '+DS' in result,
            'ES': '+ES' in result,
            'CIS707-A': '+CIS707-A' in result,
            'CIS-856': '+CIS-856' in result,
            'MS': '+MS' in result,
        }

        return capabilities
