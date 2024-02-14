"""
This file contains classes related to V.25TER commands.

This file may raise V25TERException,
remember to capture accordingly.
"""

import time

import py_sim7600.controller as controller
from py_sim7600.exceptions import V25TERException, DeviceException


class V25TERController(controller.DeviceController):
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

    def dial_from(self, target: str | int, memory: str = None, voice=True) -> bool:
        """
        Originate call from specified memory or active memory

        Corresponding command: ATD>

        :param voice: Control whether to make a data call
        :param memory: The memory to pull number from. Leave empty to use active memory
        :param target: The target to call
        :return: True if call is successful
        :rtype: bool
        :raises AssertionError: Memory type error
        """

        from py_sim7600._command_lists import memory_list

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
            assert memory in memory_list, 'Memory type error'

            command += memory + target

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
            command="ATH",
            back="OK"
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

        command = "ATS0="

        if times > 255 or times < 0:
            raise V25TERException("Auto answer times out of range")

        command += str(times).zfill(3)

        self.device.send(
            command=command,
            back="OK",
        )

        return True

    def check_auto_answer(self) -> int:
        """
        Check the auto answer configuration

        Corresponding command: ATS0

        :return: Results from device return buffer
        :rtype: int
        :raises V25TERException: Auto answer time set to too long or too short
        """

        command = "ATS0?"

        result = self.device.send(
            command=command,
            back="OK",
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
            command="+++",
            back="OK",
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
            command="ATO",
            back="CONNECT",
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
            command="ATI",
            back="OK",
        )

        result_dict = {}

        for line in result.split("\r"):
            if line != "OK":
                key, value = line.split(": ")

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

        command = "AT+IPR=" + str(baud)

        self.device.send(
            command=command,
            back="OK",
        )

        return True

    def check_baud(self) -> int:
        """
        Check the current baud rate setting

        Corresponding command: AT+IPR?

        :return: The current baud rate setting
        :rtype: int
        """

        result = self.device.send(
            command="AT+IPR?",
            back="OK",
        )

        return int(result.split(":")[1])

    def set_control_character(self, format_control: int, parity=-1) -> bool:
        """
        Set control character framing

        Corresponding command: AT+ICF

        :param parity: Parity bit format
        :param format_control: Control format
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Parity code error or Format code error
        """

        command = "AT+ICF="

        if format_control < 0 or format_control > 6:
            raise V25TERException("Format code error")
        elif format_control == 2 or format_control == 5:
            if parity == -1:
                raise V25TERException("Parity code need to be set for this format")
            else:
                command += f'{format_control},{parity}'
        else:
            if parity != -1:
                raise V25TERException("Parity code no need to be set for this format")
            else:
                command += str(format_control)

        result = self.device.send(
            command=command,
            back="OK",
        )

        return result

    def check_control_character(self) -> (int, int):
        """
        Check the current control character framing setting

        Corresponding command: AT+ICF?

        :return: The current control character framing setting
        :rtype: tuple
        """

        result = self.device.send(
            command="AT+ICF?",
            back="OK",
        )

        settings = result.split(":")[1].split(",")

        return int(settings[0]), int(settings[1])

    def set_data_flow(self, dce: int, dte=0) -> bool:
        """
        Set local data flow control

        Corresponding command: AT+IFC

        :param dce: DCE value
        :param dte: DTE value
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Control value error
        """

        command = "AT+IFC="

        if (dce != 0 and dce != 2) or (dte != 0 and dte != 2):
            raise V25TERException("Control value error")
        else:
            command += f'{dce},{dte}'

        self.device.send(
            command=command,
            back="OK",
        )

        return True

    def check_data_flow(self) -> (int, int):
        """
        Check the current data flow control setting

        Corresponding command: AT+IFC?

        :return: The current data flow control setting
        :rtype: tuple
        """

        result = self.device.send(
            command="AT+IFC?",
            back="OK",
        )

        settings = result.split(":")[1].split(",")

        return int(settings[0]), int(settings[1])

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
            raise V25TERException("DCD value error")

        self.device.send(
            command="AT&C" + str(dcd),
            back="OK",
        )

        return True

    def enable_command_echo(self, enable: int) -> bool:
        """
        Enable command echo

        Corresponding command: ATE

        :param enable: Controls whether the command echo should be enabled
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Device echo value error
        """

        if enable != 0 and enable != 1:
            raise V25TERException("Device echo value error")

        self.device.send(
            command="ATE" + str(enable),
            back="OK",
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
            command="AT&V",
            back="OK",
        )

        config = {}

        for conf_str in result.split(';'):
            conf_arr = conf_str.split(':')
            if len(conf_arr) == 2:
                attribute = conf_arr[0].strip()
                value = conf_arr[1].strip()

                config[attribute] = value

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
            raise V25TERException("DTR Mode value error")

        self.device.send(
            command="AT&D" + str(dtr),
            back="OK",
        )

        return True

    def set_dsr(self, dsr: int) -> bool:
        """
        Set DSR function mode

        Corresponding command: AT&S

        :param dsr: The mode to set DSR display
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: DSR display mode value error
        """

        if dsr != 0 and dsr != 1:
            raise V25TERException("DSR display mode value error")

        self.device.send(
            command="AT&S" + str(dsr),
            back="OK",
        )

        return True

    def set_result_format(self, r_format: int) -> bool:
        """
        Set result code format mode

        Corresponding command: ATV

        :param r_format: The format to set the result output
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Result format display mode value error
        """

        if r_format != 0 and r_format != 1:
            raise V25TERException("Result format display mode value error")

        self.device.send(
            command="ATV" + str(r_format),
            back="",
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

        command = "AT&F"

        if temporary:
            command += "0"

        self.device.send(
            command=command,
            back="OK",
        )

        return True

    def set_result_presentation(self, dce=0) -> bool:
        """
        Set Result Code Presentation Mode

        Corresponding command: ATQ

        :param dce: Set whether DCE return code is transmitted
        :return: True if setting is successful
        :rtype: bool
        :raises V25TERException: Result format display mode value error
        """

        if dce != 0 and dce != 1:
            raise V25TERException("Result format display mode value error")

        self.device.send(
            command="ATQ" + str(dce),
            back="",
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
            raise V25TERException("Connect mode value error")

        self.device.send(
            command="ATX" + str(mode),
            back="OK",
        )

        return True

    def set_connect_protocol(self, report=0):
        """
        Set CONNECT Result Code Format About Protocol

        Corresponding command: AT\\V

        :param report: Set whether to report communication protocol
        :return: Results from device return buffer
        :raises V25TERException: Report mode value error
        """

        if report != 0 and report != 1:
            raise V25TERException("Report mode value error")

        self.device.send(
            command="AT\\V" + str(report),
            back="OK",
        )

        return self.device.result()

    def set_connect_speed(self, speed=1):
        """
        Set CONNECT Result Code Format About Speed

        Corresponding command: AT&E

        :param speed: The speed to set
        :return: Results from device return buffer
        :raises V25TERException: Speed mode value error
        """

        if speed != 0 and speed != 1:
            raise V25TERException("Speed mode value error")

        self.device.send(
            command="AT&E" + str(speed),
            back="OK",
        )

        return self.device.result()

    def save_config(self):
        """
        Save the user setting to ME

        Corresponding command: AT&W

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT&W",
            back="OK",
        )

        return self.device.result()

    def restore_config(self):
        """
        Restore the user setting from ME

        Corresponding command: ATZ

        :return: Results from device return buffer
        """

        self.device.send(
            command="ATZ",
            back="OK",
        )

        return self.device.result()

    def get_manufacturer(self):
        """
        Request manufacturer identification

        Corresponding command: AT+CGMI

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CGMI",
            back="OK",
        )

        return self.device.result()

    def get_model(self):
        """
        Request model identification

        Corresponding command: AT+CGMM

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CGMM",
            back="OK",
        )

        return self.device.result()

    def get_revision(self):
        """
        Request revision identification

        Corresponding command: AT+CGMR

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CGMR",
            back="OK",
        )

        return self.device.result()

    def get_serial(self):
        """
        Request product serial number identification

        Corresponding command: AT+CGSN

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CGSN",
            back="OK",
        )

        return self.device.result()

    def set_te(self, char_set: str, check=False):
        """
        Select TE character set

        Corresponding command: AT+CSCS

        :param check: Set whether to check the current setting
        :param char_set: The character set to use
        :return: Results from device return buffer
        :raises V25TERException: Character set parameter error
        """

        command = "AT+CSCS"

        if check:
            command += "?"
        elif char_set == "IRA" or char_set == "GSM" or char_set == "UCS2":
            command += '="' + char_set
        else:
            raise V25TERException("Character set parameter error")

        self.device.send(
            command=command,
            back="OK",
        )

        return self.device.result()

    def get_international_subscriber(self):
        """
        Request international mobile subscriber identity

        Corresponding command: AT+CIMI

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CIMI",
            back="OK",
        )

        return self.device.result()

    def get_another_subscriber(self):
        """
        Request another international mobile subscriber identity

        Corresponding command: AT+CIMIM

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CIMIM",
            back="OK",
        )

        return self.device.result()

    def get_capabilities(self):
        """
        Request overall capabilities

        Corresponding command: AT+GCAP

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+GCAP",
            back="OK",
        )

        return self.device.result()
