"""
This file contains classes related to status control commands.

This file may raise StatusControlException,
remember to capture accordingly.
"""

import re
from typing import Union

from py_sim7600.controller import DeviceController
from py_sim7600.exceptions import StatusControlException, DeviceException
from py_sim7600.model import enums


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
            raise StatusControlException(f'Error setting function: {e}')

        return True

    def get_function(self) -> enums.PhoneFunctionalityLevel:
        """
        Get phone functionality

        Corresponding command: AT+CFUN?

        :return: Function level
        :rtype: enums.PhoneFunctionalityLevel
        """

        result = self.device.send(
            command='AT+CFUN?',
            back='OK',
            error_pattern=['ERROR']
        )

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
        result = self.device.send(
            command='AT+CPIN?',
            back='OK',
            error_pattern=['ERROR']
        )

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

        self.device.send(
            command=command,
            back="OK",
            error_pattern=['ERROR']
        )

        return True

    def get_iccid(self) -> str:
        """
        Read ICCID from SIM card

        Corresponding command: AT+CICCID

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CICCID",
            back="OK"
        )

        return self.device.result()

    def sim_access_general(self, command: str) -> str:
        """
        Generic SIM access

        Corresponding command: AT+CSIM

        :param command: Command passed from MT to SIM card
        :return: Results from device return buffer
        """

        # TODO: Add a more detailed check to SIM-ME commands.

        length = len(command)

        self.device.send(
            command="AT+CSIM=" + str(length) + "," + command,
            back="OK"
        )

        return self.device.result()

    def sim_access_restricted(self,
                              command: int,
                              file_id: int = None,
                              p1: int = None,
                              p2: int = None,
                              p3: int = None,
                              data: str = None,
                              ) -> str:
        """
        Restricted SIM access

        Corresponding command: AT+CRSM

        :param command: Command passed on by the MT to the SIM
        :param file_id: Identifier for an elementary data file on SIM, if used by the command
        :param p1: First parameter for the command
        :param p2: Second parameter for the command
        :param p3: Third parameter for the command
        :param data: Data to be written to the SIM
        :return: Results from device return buffer
        """

        from py_sim7600._command_lists import restricted_sim_command, restricted_sim_file_id

        assert command in restricted_sim_command.keys(), "Illegal Command"

        command_out = "AT+CRSM=" + str(command)

        if file_id is not None:
            assert file_id in restricted_sim_file_id.keys(), "Illegal File ID"

            command_out += "," + str(file_id)
        if p1 is not None:
            command_out += "," + str(p1)
        if p2 is not None:
            command_out += "," + str(p2)
        if p3 is not None:
            command_out += "," + str(p3)
        if data is not None:
            command_out += ',"' + str(data) + '"'

        self.device.send(
            command=command_out,
            back="OK"
        )

        return self.device.result()

    def pin_times(self) -> str:
        """
        Times remain to input SIM PIN/PUK

        Corresponding command: AT+SPIC

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+SPIC",
            back="OK"
        )

        return self.device.result()

    def get_provider(self) -> str:
        """
        Get service provider name from SIM

        Corresponding command: AT+CSPN

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CSPN?",
            back="OK"
        )

        return self.device.result()

    def get_signal(self) -> str:
        """
        Query signal quality

        Corresponding command: AT+CSQ

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CSQ",
            back="OK"
        )

        return self.device.result()

    def set_csq(self, auto=0, csq=0, check=False) -> str:
        """
        Set CSQ report

        Corresponding command: AT+AUTOCSQ

        :return: Results from device return buffer
        :raises StatusControlException: Auto or CSQ mode setting error
        """

        if check:
            self.device.send(
                command="AT+AUTOCSQ?",
                back="OK"
            )

            return self.device.result()
        
        if auto != 0 and auto != 1:
            raise StatusControlException("Auto setting error")
        if csq != 0 and csq != 1:
            raise StatusControlException("CSQ setting error")

        command = "AT+AUTOCSQ=" + str(auto) + "," + str(csq)

        self.device.send(
            command=command,
            back="OK"
        )

        return self.device.result()

    def set_rssi(self, delta=5, check=False) -> str:
        """
        Set RSSI delta change threshold

        Corresponding command: AT+CSQDELTA

        :return: Results from device return buffer
        :raises StatusControlException: Delta value error
        """

        if check:
            self.device.send(
                command="AT+CSQDELTA?",
                back="OK"
            )

            return self.device.result()

        if delta < 0 or delta > 5:
            raise StatusControlException("Delta value error")

        self.device.send(
            command="AT+CSQDELTA=" + str(delta),
            back="OK"
        )

        return self.device.result()

    def set_urc(self, port: int, check=False) -> str:
        """
        Configure URC destination interface

        Corresponding command: AT+CATR

        :return: Results from device return buffer
        :raises StatusControlException: Port setting error
        """

        if check:
            self.device.send(
                command="AT+CATR?",
                back="OK"
            )

            return self.device.result()

        from py_sim7600._command_lists import urc_ports

        if port not in urc_ports.keys():
            raise StatusControlException("Port setting error")
        
        self.device.send(
            command="AT+CATR=" + str(port),
            back="OK"
        )

        return self.device.result()

    def power_down(self) -> str:
        """
        Power down the module

        Corresponding command: AT+CPOF

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CPOF",
            back="OK"
        )

        return self.device.result()

    def reset(self) -> str:
        """
        Reset the module

        Corresponding command: AT+CRESET

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CRESET",
            back="OK"
        )

        return self.device.result()

    def accumulated_meter(self, password: str, check=False) -> str:
        """
        Accumulated call meter

        Corresponding command: AT+CACM

        :return: Results from device return buffer
        """

        if check:
            self.device.send(
                command="AT+CACM?",
                back="OK"
            )

            return self.device.result()

        command = "AT+CACM"
        
        if password != None:
            command += '="' + password + '"'

        self.device.send(
            command=command,
            back="OK"
        )

        return self.device.result()

    def set_maximum(self, max: str, password: str, check=False) -> str:
        """
        Accumulated call meter maximum

        Corresponding command: AT+CAMM

        :return: Results from device return buffer
        """

        if check:
            self.device.send(
                command="AT+CAMM?",
                back="OK"
            )

            return self.device.result()
        
        command = 'AT+CAMM="' + max + '"'

        if password is not None:
            command += ',"' + password + '"'
        
        self.device.send(
            command=command,
            back="OK"
        )

        return self.device.result()

    def set_price(self, currency: str, ppu: str, password: str, check=False) -> str:
        """
        Price per unit and currency table

        Corresponding command: AT+CPUC

        :return: Results from device return buffer
        """

        if check:
            self.device.send(
                command="AT+CPUC?",
                back="OK"
            )

            return self.device.result()
        
        command = 'AT+CPUC="' + currency + '","' + ppu + '"'

        if password != None:
            command += ',"' + password + '"'
        
        self.device.send(
            command=command,
            back="OK"
        )

        return self.device.result()

    def real_time_clock(self, time: str, check=False) -> str:
        """
        Real time clock management

        Corresponding command: AT+CCLK

        :return: Results from device return buffer
        """

        if check:
            self.device.send(
                command="AT+CCLK?",
                back="OK"
            )

            return self.device.result()
        
        command = 'AT+CCLK="' + time + '"'

        self.device.send(
            command=command,
            back="OK"
        )

        return self.device.result()

    def set_error_report(self, code=2, check=False) -> str:
        """
        Report mobile equipment error

        Corresponding command: AT+CMEE

        :return: Results from device return buffer
        :raises StatusControlException: Error level parameter error
        """

        if check:
            self.device.send(
                command="AT+CMEE?",
                back="OK"
            )

            return self.device.result()
        
        if code != 0 and code != 1 and code != 2:
            raise StatusControlException("Error level parameter error")

        command = 'AT+CCLK=' + str(code)

        self.device.send(
            command=command,
            back="OK"
        )

        return self.device.result()

    def get_activity(self) -> str:
        """
        Phone activity status

        Corresponding command: AT+CPAS

        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+CPAS",
            back="OK"
        )

        return self.device.result()

    def set_imei(self, imei:str, check=False) -> str:
        """
        Set IMEI for the module

        Corresponding command: AT+SIMEI

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        if check:
            self.device.send(
                command="AT+SIMEI?",
                back="OK"
            )

            return self.device.result()
        
        self.device.send(
            command="AT+SIMEI=" + imei,
            back="OK"
        )

        return self.device.result()

    def get_equipment_id(self) -> str:
        """
        Request Mobile Equipment Identifier

        Corresponding command: AT+SMEID

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        """

        self.device.send(
            command="AT+SMEID?",
            back="OK"
        )

        return self.device.result()

    def voicemail_number(self, number: str, valid: bool, type: int, check=False) -> str:
        """
        Voice Mail Subscriber number

        Corresponding command: AT+CSVM

        :return: Results from device return buffer
        :raises StatusControlException:
        """

        if check:
            self.device.send(
                command="AT+CSVM?",
                back="OK"
            )

            return self.device.result()
        
        command = "AT+CSVM="

        if valid:
            command += '1,"'
        else:
            command += '0,"'
        
        command += number + '",' + str(type)

        self.device.send(
            command=command,
            back="OK"
        )

        return self.device.result()
