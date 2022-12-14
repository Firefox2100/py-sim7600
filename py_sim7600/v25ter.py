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

    @staticmethod
    def re_issue(device: Device) -> str:
        """
        Re-issues the Last Command Given

        Corresponding command: A/

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        device.send(
            command="A/",
            back="OK",
        )

        return device.result()

    @staticmethod
    def dial(device: Device, number: str, anonymous=False, cug_invocation=False, voice=True) -> str:
        """
        Mobile Originated Call to Dial A Number

        Corresponding command: ATD

        :param voice: Control whether to make a data call
        :param cug_invocation: Control whether this call should invoke Closed User Group
        :param anonymous: Control whether to display caller number
        :param number: Number to call
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        command = "ATD" + number
        back = "OK"
        if anonymous:
            command += "I"

        if cug_invocation:
            command += "G"

        if voice:
            command += ";"
        else:
            back = "CONNECT"

        device.send(
            command=command,
            back=back,
        )

        return device.result()

    @staticmethod
    def dial_from(device: Device, target: Union[str, int], memory="", voice=True) -> str:
        """
        Originate call from specified memory or active memory

        Corresponding command: ATD>

        :param voice: Control whether to make a data call
        :param memory: The memory to pull number from. Leave empty to use active memory
        :param target: The target to call
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Poorly formatted command
        """

        from py_sim7600._command_lists import memory_list

        command = "ATD>"
        back = "OK"

        if memory == "":
            # From active memory
            command += str(target)
        elif memory in memory_list:
            if type(target) == int:
                command += memory + str(target)
            else:
                raise V25TERException("ATD with specified memory can't be used to call a named contact")
        else:
            raise V25TERException("Memory type error")

        if voice:
            command += ";"
        else:
            back = "CONNECT"

        device.send(
            command=command,
            back=back,
        )

        return device.result()

    @staticmethod
    def answer(device: Device) -> str:
        """
        Call answer

        Corresponding command: ATA

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: No incoming call
        """

        device.send(
            command="ATA",
            back="OK",
        )

        result = device.result()

        if result == "NO CARRIER":
            raise V25TERException("No incoming call or no reception")

        return result

    @staticmethod
    def disconnect(device: Device) -> str:
        """
        Disconnect existing call

        Corresponding command: ATH

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        from py_sim7600.call_control import CallControl

        CallControl.control_voice_hangup(
            device=device,
            mode="?"
        )

        result = ""

        if device.result() != "+CVHU: 0":
            result += "Warning: CVHU is set to 1. Voice call may still be active. \n"

        device.send(
            command="ATH",
            back="OK"
        )

        return result + device.result()

    @staticmethod
    def auto_answer(device: Device, times: Union[int, str]) -> str:
        """
        Automatic answer incoming call

        Corresponding command: ATS0

        :param times: Times to automatically answer the call. Set to 0 to disable it. Pass '?' to query current setting.
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Auto answer time set to too long or too short
        """

        command = "ATS0"

        if type(times) == str:
            command += times
        else:
            if times > 255 or times < 0:
                raise V25TERException("Auto answer times out of range")

            command += "=" + times.zfill(3)

        device.send(
            command=command,
            back="OK",
        )

        return device.result()

    @staticmethod
    def switch_to_command(device: Device) -> str:
        """
        Switch from data mode to command mode

        Corresponding command: +++

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        time.sleep(1)

        device.send(
            command="+++",
            back="OK",
        )

        return device.result()

    @staticmethod
    def switch_to_data(device: Device) -> str:
        """
        Switch from command mode to data mode

        Corresponding command: ATO

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="ATO",
            back="CONNECT",
        )

        return device.result()

    @staticmethod
    def info(device: Device) -> str:
        """
        Display product identification information

        Corresponding command: ATI

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="ATI",
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_baud(device: Device, baud: Union[str, int]) -> str:
        """
        Set local baud rate temporarily

        Corresponding command: AT+IPR

        :param baud: The baud rate to set. Pass '?' = query current setting.
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        command = "AT+IPR"

        if type(baud) == str:
            command += baud
        else:
            command += "=" + baud

        device.send(
            command=command,
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_control_character(device: Device, format_control: int, parity=-1, check=False) -> str:
        """
        Set control character framing

        Corresponding command: AT+ICF

        :param check: Set it to true to check current settings
        :param parity: Parity bit format
        :param format_control: Control format
        :param device: A SIM7600 device instance
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

        device.send(
            command=command,
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_data_flow(device: Device, dce: int, dte=0, check=False) -> str:
        """
        Set local data flow control

        Corresponding command: AT+IFC

        :param check: Set it to true to check current settings
        :param dce: DCE value
        :param dte: DTE value
        :param device: A SIM7600 device instance
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

        device.send(
            command=command,
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_dcd_function(device: Device, dcd: int):
        """
        Set DCD function mode

        Corresponding command: AT&C

        :param dcd: The DCD setting to be set
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: DCD value error
        """

        if dcd < 0 or dcd > 2:
            raise V25TERException("DCD value error")

        device.send(
            command="AT&C" + str(dcd),
            back="OK",
        )

        return device.result()

    @staticmethod
    def enable_command_echo(device: Device, enable: int):
        """
        Enable command echo

        Corresponding command: ATE

        :param enable: Controls whether the command echo should be enabled
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Device echo value error
        """

        if enable != 0 and enable != 1:
            raise V25TERException("Device echo value error")

        device.send(
            command="ATE" + str(enable),
            back="OK",
        )

        return device.result()

    @staticmethod
    def current_config(device: Device):
        """
        Display current configuration

        Corresponding command: AT&V

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT&V",
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_dtr(device: Device, dtr: int):
        """
        Set DTR function mode

        Corresponding command: AT&D

        :param dtr: The mode to set DTR PIN function behaviour
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: DTR Mode value error
        """

        if dtr < 0 or dtr > 2:
            raise V25TERException("DTR Mode value error")

        device.send(
            command="AT&D" + str(dtr),
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_dsr(device: Device, dsr: int):
        """
        Set DSR function mode

        Corresponding command: AT&S

        :param dsr: The mode to set DSR display
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: DSR display mode value error
        """

        if dsr != 0 and dsr != 1:
            raise V25TERException("DSR display mode value error")

        device.send(
            command="AT&S" + str(dsr),
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_result_format(device: Device, r_format: int):
        """
        Set result code format mode

        Corresponding command: ATV

        :param r_format: The format to set the result output
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Result format display mode value error
        """

        if r_format != 0 and r_format != 1:
            raise V25TERException("Result format display mode value error")

        device.send(
            command="ATV" + str(r_format),
            back="",
        )

        return device.result()

    @staticmethod
    def reset_config(device: Device, temporary=False):
        """
        Set all current parameters to manufacturer defaults

        Corresponding command: AT&F

        :param temporary: Set some temporary TA parameters to manufacturer defaults
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        command = "AT&F"

        if temporary:
            command += "0"

        device.send(
            command=command,
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_result_presentation(device: Device, dce=0):
        """
        Set Result Code Presentation Mode

        Corresponding command: ATQ

        :param dce: Set whether DCE return code is transmitted
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Result format display mode value error
        """

        if dce != 0 and dce != 1:
            raise V25TERException("Result format display mode value error")

        device.send(
            command="ATQ" + str(dce),
            back="",
        )

        return device.result()

    @staticmethod
    def set_connect_format(device: Device, mode=1):
        """
        Set CONNECT Result Code Format

        Corresponding command: ATX

        :param mode: Set whether CONNECT is returned
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Connect mode value error
        """

        if mode < 0 or mode > 4:
            raise V25TERException("Connect mode value error")

        device.send(
            command="ATX" + str(mode),
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_connect_protocol(device: Device, report=0):
        """
        Set CONNECT Result Code Format About Protocol

        Corresponding command: AT\\V

        :param report: Set whether to report communication protocol
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Report mode value error
        """

        if report != 0 and report != 1:
            raise V25TERException("Report mode value error")

        device.send(
            command="AT\\V" + str(report),
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_connect_speed(device: Device, speed=1):
        """
        Set CONNECT Result Code Format About Speed

        Corresponding command: AT&E

        :param speed: The speed to set
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Speed mode value error
        """

        if speed != 0 and speed != 1:
            raise V25TERException("Speed mode value error")

        device.send(
            command="AT&E" + str(speed),
            back="OK",
        )

        return device.result()

    @staticmethod
    def save_config(device: Device):
        """
        Save the user setting to ME

        Corresponding command: AT&W

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT&W",
            back="OK",
        )

        return device.result()

    @staticmethod
    def restore_config(device: Device):
        """
        Restore the user setting from ME

        Corresponding command: ATZ

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="ATZ",
            back="OK",
        )

        return device.result()

    @staticmethod
    def get_manufacturer(device: Device):
        """
        Request manufacturer identification

        Corresponding command: AT+CGMI

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+CGMI",
            back="OK",
        )

        return device.result()

    @staticmethod
    def get_model(device: Device):
        """
        Request model identification

        Corresponding command: AT+CGMM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+CGMM",
            back="OK",
        )

        return device.result()

    @staticmethod
    def get_revision(device: Device):
        """
        Request revision identification

        Corresponding command: AT+CGMR

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+CGMR",
            back="OK",
        )

        return device.result()

    @staticmethod
    def get_serial(device: Device):
        """
        Request product serial number identification

        Corresponding command: AT+CGSN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+CGSN",
            back="OK",
        )

        return device.result()

    @staticmethod
    def set_te(device: Device, set: str, check=False):
        """
        Select TE character set

        Corresponding command: AT+CSCS

        :param check: Set whether to check the current setting
        :param set: The character set to use
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises V25TERException: Character set parameter error
        """

        command = "AT+CSCS"

        if check:
            command += "?"
        elif set == "IRA" or set == "GSM" or set == "UCS2":
            command += "=" + set
        else:
            raise V25TERException("Character set parameter error")

        device.send(
            command=command,
            back="OK",
        )

        return device.result()

    @staticmethod
    def get_international_subscriber(device: Device):
        """
        Request international mobile subscriber identity

        Corresponding command: AT+CIMI

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+CIMI",
            back="OK",
        )

        return device.result()

    @staticmethod
    def get_another_subscriber(device: Device):
        """
        Request another international mobile subscriber identity

        Corresponding command: AT+CIMIM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+CIMIM",
            back="OK",
        )

        return device.result()

    @staticmethod
    def get_capabilities(device: Device):
        """
        Request overall capabilities

        Corresponding command: AT+GCAP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+GCAP",
            back="OK",
        )

        return device.result()
