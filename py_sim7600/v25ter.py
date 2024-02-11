"""
This file contains classes related to V.25TER commands. This file may raise V25TERException,
remember to capture accordingly.
"""

from py_sim7600.device import Device
from py_sim7600.error import V25TERException
from typing import Union
import time


class V25TER:
    """
    AT Commands According to V.25TER
    """

    def __init__(self, device: Device):
        self.device = device

    def re_issue(self) -> str:
        """
        Re-issues the Last Command Given

        Corresponding command: A/

        :return: Results of the last command
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

    def dial_from(self, target: Union[str, int], memory: str = None, voice=True) -> bool:
        """
        Originate call from specified memory or active memory

        Corresponding command: ATD>

        :param voice: Control whether to make a data call
        :param memory: The memory to pull number from. Leave empty to use active memory
        :param target: The target to call
        :return: True if call is successful
        :raises AssertionError: Memory type error
        """

        from py_sim7600._command_lists import memory_list

        command = 'ATD>'
        back = 'OK'

        if memory is None:
            # From active memory
            command += str(target)
        else:
            assert memory in memory_list, 'Memory type error'

            command += memory + str(target)

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
        :raises V25TERException: No incoming call
        """

        result = self.device.send(
            command='ATA',
            back='OK',
        )

        if 'NO CARRIER' in result:
            raise V25TERException("No incoming call or no reception")

        return True

    def disconnect(self) -> bool:
        """
        Disconnect existing call

        Corresponding command: ATH

        :return: True if call is disconnected
        """

        from py_sim7600.call_control import CallControl

        call_controller = CallControl(self.device)

        try:
            call_controller.control_voice_hangup(mode=0)
        except Exception as e:
            if not call_controller.check_control_voice_hangup():
                raise e

        self.device.send(
            command="ATH",
            back="OK"
        )

        return True

    def auto_answer(self, times: int) -> str:
        """
        Automatic answer incoming call

        Corresponding command: ATS0

        :param times: Times of ring to auto answer. Set to 0 to disable auto answer.
        :return: Results from device return buffer
        :raises V25TERException: Auto answer time set to too long or too short
        """

        command = "ATS0="

        if times > 255 or times < 0:
            raise V25TERException("Auto answer times out of range")

        command += str(times).zfill(3)

        result = self.device.send(
            command=command,
            back="OK",
        )

        return result

    def check_auto_answer(self) -> int:
        """
        Check the auto answer configuration

        Corresponding command: ATS0

        :return: Results from device return buffer
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
        """

        self.device.send(
            command="ATO",
            back="CONNECT",
        )

        return True

    def info(self) -> str:
        """
        Display product identification information

        Corresponding command: ATI

        :return: Identification information
        """

        result = self.device.send(
            command="ATI",
            back="OK",
        )

        return result

    def set_baud(self, baud: int) -> bool:
        """
        Set local baud rate temporarily

        Corresponding command: AT+IPR

        :param baud: The baud rate to set.
        :return: Results from device return buffer
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
        """

        result = self.device.send(
            command="AT+IPR?",
            back="OK",
        )

        return int(result.split(":")[1])

    def set_control_character(self, format_control: int, parity=-1, check=False) -> str:
        """
        Set control character framing

        Corresponding command: AT+ICF

        :param check: Set it to true to check current settings
        :param parity: Parity bit format
        :param format_control: Control format
        :return: Results from device return buffer
        :raises V25TERException: Parity code error
        """

        command = "AT+ICF"

        if check:
            command += "?"
        elif format_control < 0 or format_control > 6:
            raise V25TERException("Format code error")
        elif format_control == 2 or format_control == 5:
            if parity == -1:
                raise V25TERException("Parity code need to be set for this format")
            else:
                command += "=" + str(format_control) + "," + str(parity)
        else:
            if parity != -1:
                raise V25TERException("Parity code no need to be set for this format")
            else:
                command += "=" + str(format_control)

        self.device.send(
            command=command,
            back="OK",
        )

        return self.device.result()

    def set_data_flow(self, dce: int, dte=0, check=False) -> str:
        """
        Set local data flow control

        Corresponding command: AT+IFC

        :param check: Set it to true to check current settings
        :param dce: DCE value
        :param dte: DTE value
        :return: Results from device return buffer
        :raises V25TERException: Control value error
        """

        command = "AT+IFC"

        if check:
            command += "?"
        elif (dce != 0 and dce != 2) or (dte != 0 and dte != 2):
            raise V25TERException("Control value error")
        else:
            command += "=" + str(dce) + "," + str(dte)

        self.device.send(
            command=command,
            back="OK",
        )

        return self.device.result()

    def set_dcd_function(self, dcd: int):
        """
        Set DCD function mode

        Corresponding command: AT&C

        :param dcd: The DCD setting to be set
        :return: Results from device return buffer
        :raises V25TERException: DCD value error
        """

        if dcd < 0 or dcd > 2:
            raise V25TERException("DCD value error")

        self.device.send(
            command="AT&C" + str(dcd),
            back="OK",
        )

        return self.device.result()

    def enable_command_echo(self, enable: int):
        """
        Enable command echo

        Corresponding command: ATE

        :param enable: Controls whether the command echo should be enabled
        :return: Results from device return buffer
        :raises V25TERException: Device echo value error
        """

        if enable != 0 and enable != 1:
            raise V25TERException("Device echo value error")

        self.device.send(
            command="ATE" + str(enable),
            back="OK",
        )

        return self.device.result()

    def current_config(self):
        """
        Display current configuration

        Corresponding command: AT&V

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT&V",
            back="OK",
        )

        return self.device.result()

    def set_dtr(self, dtr: int):
        """
        Set DTR function mode

        Corresponding command: AT&D

        :param dtr: The mode to set DTR PIN function behaviour
        :return: Results from device return buffer
        :raises V25TERException: DTR Mode value error
        """

        if dtr < 0 or dtr > 2:
            raise V25TERException("DTR Mode value error")

        self.device.send(
            command="AT&D" + str(dtr),
            back="OK",
        )

        return self.device.result()

    def set_dsr(self, dsr: int):
        """
        Set DSR function mode

        Corresponding command: AT&S

        :param dsr: The mode to set DSR display
        :return: Results from device return buffer
        :raises V25TERException: DSR display mode value error
        """

        if dsr != 0 and dsr != 1:
            raise V25TERException("DSR display mode value error")

        self.device.send(
            command="AT&S" + str(dsr),
            back="OK",
        )

        return self.device.result()

    def set_result_format(self, r_format: int):
        """
        Set result code format mode

        Corresponding command: ATV

        :param r_format: The format to set the result output
        :return: Results from device return buffer
        :raises V25TERException: Result format display mode value error
        """

        if r_format != 0 and r_format != 1:
            raise V25TERException("Result format display mode value error")

        self.device.send(
            command="ATV" + str(r_format),
            back="",
        )

        return self.device.result()

    def reset_config(self, temporary=False):
        """
        Set all current parameters to manufacturer defaults

        Corresponding command: AT&F

        :param temporary: Set some temporary TA parameters to manufacturer defaults
        :return: Results from device return buffer
        """

        command = "AT&F"

        if temporary:
            command += "0"

        self.device.send(
            command=command,
            back="OK",
        )

        return self.device.result()

    def set_result_presentation(self, dce=0):
        """
        Set Result Code Presentation Mode

        Corresponding command: ATQ

        :param dce: Set whether DCE return code is transmitted
        :return: Results from device return buffer
        :raises V25TERException: Result format display mode value error
        """

        if dce != 0 and dce != 1:
            raise V25TERException("Result format display mode value error")

        self.device.send(
            command="ATQ" + str(dce),
            back="",
        )

        return self.device.result()

    def set_connect_format(self, mode=1):
        """
        Set CONNECT Result Code Format

        Corresponding command: ATX

        :param mode: Set whether CONNECT is returned
        :return: Results from device return buffer
        :raises V25TERException: Connect mode value error
        """

        if mode < 0 or mode > 4:
            raise V25TERException("Connect mode value error")

        self.device.send(
            command="ATX" + str(mode),
            back="OK",
        )

        return self.device.result()

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
