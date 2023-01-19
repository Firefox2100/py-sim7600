"""
This file contains classes related to status control commands. This file may raise StatusControlException,
remember to capture accordingly.
"""

from py_sim7600.device import Device
from py_sim7600.error import StatusControlException
from typing import Union


class StatusControl:
    """
    AT Commands for Status Control
    """

    @staticmethod
    def set_function(device: Device, function: int, reset: bool) -> str:
        """
        Set phone functionality

        Corresponding command: AT+CFUN

        :param reset: Controls whether to reset the memory
        :param function: The function level to set the modem into
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises StatusControlException: Reset or restart required
        """

        command = "AT+CFUN"

        device.send(
            command="AT+CFUN?",
            back="OK"
        )

        status = device.result()

        if function != 7 and function != 6 and "7" in status:
            # Restart required
            raise StatusControlException("Reset or restart required")

        command += "=" + str(function)

        if reset:
            command += ",1"

        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def enter_pin(device: Device, pin: str, puk="") -> str:
        """
        Enter PIN

        If this is a new SIM card, then PUK might be necessary.
        Set PIN to the new PIN, and set PUK to the current PUK.

        Corresponding command: AT+CPIN

        :param puk: The current PUK (temporary PIN), if applicable
        :param pin: The PIN of the SIM card. If PUK is present, this is the new PIN to set.
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises StatusControlException: PUK required
        """
        
        command = "AT+CPIN"

        device.send(
            command="AT+CPIN?",
            back="OK"
        )

        if "PUK" in device.result():
            if puk == "":
                raise StatusControlException("PUK required")
            else:
                command += "=" + puk + "," + pin
        else:
            command += "=" + pin
        
        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def get_iccid(device: Device) -> str:
        """
        Read ICCID from SIM card

        Corresponding command: AT+CICCID

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        device.send(
            command="AT+CICCID",
            back="OK"
        )

        return device.result()

    @staticmethod
    def sim_access_general(device: Device, length: int, command: str) -> str:
        """
        Generic SIM access

        Corresponding command: AT+CSIM

        :param command: The command to be sent
        :param length: The length of the command to be sent
        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        # TODO: Add a more detailed check to SIM-ME commands.

        device.send(
            command="AT+CSIM=" + str(length) + "," + command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def sim_access_restricted(device: Device, command: int, file_id: int, p1: int, p2: int, p3: int, data: str) -> str:
        """
        Restricted SIM access

        Corresponding command: AT+CRSM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        # TODO: Add a more detailed check to this command

        command_out = "AT+CRSM=" + str(command)

        if file_id != None:
            command_out += "," + str(file_id)
        if p1 != None:
            command_out += "," + str(p1)
        if p2 != None:
            command_out += "," + str(p2)
        if p3 != None:
            command_out += "," + str(p3)
        if data != None:
            command_out += ',"' + str(data) + '"'

        device.send(
            command=command_out,
            back="OK"
        )

        return device.result()

    @staticmethod
    def pin_times(device: Device) -> str:
        """
        Times remain to input SIM PIN/PUK

        Corresponding command: AT+SPIC

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        device.send(
            command="AT+SPIC",
            back="OK"
        )

        return device.result()

    @staticmethod
    def get_provider(device: Device) -> str:
        """
        Get service provider name from SIM

        Corresponding command: AT+CSPN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        device.send(
            command="AT+CSPN?",
            back="OK"
        )

        return device.result()

    @staticmethod
    def get_signal(device: Device) -> str:
        """
        Query signal quality

        Corresponding command: AT+CSQ

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        device.send(
            command="AT+CSQ",
            back="OK"
        )

        return device.result()

    @staticmethod
    def set_csq(device: Device, auto=0, csq=0, check=False) -> str:
        """
        Set CSQ report

        Corresponding command: AT+AUTOCSQ

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises StatusControlException: Auto or CSQ mode setting error
        """

        if check:
            device.send(
                command="AT+AUTOCSQ?",
                back="OK"
            )

            return device.result()
        
        if auto != 0 and auto != 1:
            raise StatusControlException("Auto setting error")
        if csq != 0 and csq != 1:
            raise StatusControlException("CSQ setting error")

        command = "AT+AUTOCSQ=" + str(auto) + "," + str(csq)

        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def set_rssi(device: Device, delta=5, check=False) -> str:
        """
        Set RSSI delta change threshold

        Corresponding command: AT+CSQDELTA

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises StatusControlException: Delta value error
        """
        
        if check:
            device.send(
                command="AT+CSQDELTA?",
                back="OK"
            )

            return device.result()

        if delta < 0 or delta > 5:
            raise StatusControlException("Delta value error")

        device.send(
            command="AT+CSQDELTA=" + str(delta),
            back="OK"
        )

        return device.result()

    @staticmethod
    def set_urc(device: Device, port: int, check=False) -> str:
        """
        Configure URC destination interface

        Corresponding command: AT+CATR

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises StatusControlException: Port setting error
        """

        if check:
            device.send(
                command="AT+CATR?",
                back="OK"
            )

            return device.result()

        from py_sim7600._command_lists import urc_ports

        if port not in urc_ports.keys():
            raise StatusControlException("Port setting error")
        
        device.send(
            command="AT+CATR=" + str(port),
            back="OK"
        )

        return device.result()

    @staticmethod
    def power_down(device: Device) -> str:
        """
        Power down the module

        Corresponding command: AT+CPOF

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        device.send(
            command="AT+CPOF",
            back="OK"
        )

        return device.result()

    @staticmethod
    def reset(device: Device) -> str:
        """
        Reset the module

        Corresponding command: AT+CRESET

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        device.send(
            command="AT+CRESET",
            back="OK"
        )

        return device.result()

    @staticmethod
    def accumulated_meter(device: Device, password: str, check=False) -> str:
        """
        Accumulated call meter

        Corresponding command: AT+CACM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        if check:
            device.send(
                command="AT+CACM?",
                back="OK"
            )

            return device.result()

        command = "AT+CACM"
        
        if password != None:
            command += '="' + password + '"'

        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def set_maximum(device: Device, max: str, password: str, check=False) -> str:
        """
        Accumulated call meter maximum

        Corresponding command: AT+CAMM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        if check:
            device.send(
                command="AT+CAMM?",
                back="OK"
            )

            return device.result()
        
        command = 'AT+CAMM="' + max + '"'

        if password != None:
            command += ',"' + password + '"'
        
        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def set_price(device: Device, currency: str, ppu: str, password: str, check=False) -> str:
        """
        Price per unit and currency table

        Corresponding command: AT+CPUC

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        if check:
            device.send(
                command="AT+CPUC?",
                back="OK"
            )

            return device.result()
        
        command = 'AT+CPUC="' + currency + '","' + ppu + '"'

        if password != None:
            command += ',"' + password + '"'
        
        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def real_time_clock(device: Device,time: str, check=False) -> str:
        """
        Real time clock management

        Corresponding command: AT+CCLK

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        if check:
            device.send(
                command="AT+CCLK?",
                back="OK"
            )

            return device.result()
        
        command = 'AT+CCLK="' + time + '"'

        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def set_error_report(device: Device, code=2, check=False) -> str:
        """
        Report mobile equipment error

        Corresponding command: AT+CMEE

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises StatusControlException: Error level parameter error
        """
        
        if check:
            device.send(
                command="AT+CMEE?",
                back="OK"
            )

            return device.result()
        
        if code != 0 and code != 1 and code != 2:
            raise StatusControlException("Error level parameter error")

        command = 'AT+CCLK=' + code

        device.send(
            command=command,
            back="OK"
        )

        return device.result()

    @staticmethod
    def get_activity(device: Device) -> str:
        """
        Phone activity status

        Corresponding command: AT+CPAS

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        device.send(
            command="AT+CPAS",
            back="OK"
        )

        return device.result()

    @staticmethod
    def set_imei(device: Device, imei:str, check=False) -> str:
        """
        Set IMEI for the module

        Corresponding command: AT+SIMEI

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        if check:
            device.send(
                command="AT+SIMEI?",
                back="OK"
            )

            return device.result()
        
        device.send(
            command="AT+SIMEI=" + imei,
            back="OK"
        )

        return device.result()

    @staticmethod
    def get_equipment_id(device: Device) -> str:
        """
        Request Mobile Equipment Identifier

        Corresponding command: AT+SMEID

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """
        
        device.send(
            command="AT+SMEID?",
            back="OK"
        )

        return device.result()

    @staticmethod
    def voicemail_number(device: Device, number: str, valid: bool, type: int, check=False) -> str:
        """
        Voice Mail Subscriber number

        Corresponding command: AT+CSVM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises StatusControlException:
        """
        
        if check:
            device.send(
                command="AT+CSVM?",
                back="OK"
            )

            return device.result()
        
        command = "AT+CSVM="

        if valid:
            command += '1,"'
        else:
            command += '0,"'
        
        command += number + '",' + str(type)

        device.send(
            command=command,
            back="OK"
        )

        return device.result()
