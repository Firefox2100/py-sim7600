"""
This file contains classes related to phonebook commands. This file may raise SIMApplicationToolkitException,
remember to capture accordingly.
"""

from py_sim7600.device import Device
from py_sim7600.exceptions import SIMApplicationToolkitException


class SIMApplicationToolkit:
    """
    AT Commands for SIM Application Toolkit
    """

    @staticmethod
    def sat_indication(device: Device) -> str:
        """
        SAT Indication

        Corresponding command: AT+STIN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises SIMApplicationToolkitException:
        """
        raise NotImplementedError

    @staticmethod
    def sat_info(device: Device) -> str:
        """
        Get SAT information

        Corresponding command: AT+STGI

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises SIMApplicationToolkitException:
        """
        raise NotImplementedError

    @staticmethod
    def sat_respond(device: Device) -> str:
        """
        SAT respond

        Corresponding command: AT+STGR

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises SIMApplicationToolkitException:
        """
        raise NotImplementedError

    @staticmethod
    def sat_switch(device: Device) -> str:
        """
        STK switch

        Corresponding command: AT+STK

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises SIMApplicationToolkitException:
        """
        raise NotImplementedError

    @staticmethod
    def set_stk_pdu(device: Device) -> str:
        """
        Set STK pdu format

        Corresponding command: AT+STKFMT

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises SIMApplicationToolkitException:
        """
        raise NotImplementedError

    @staticmethod
    def stk_pdu_envelope(device: Device) -> str:
        """
        Original STK PDU Envelope Command

        Corresponding command: AT+STENV

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises SIMApplicationToolkitException:
        """
        raise NotImplementedError

    @staticmethod
    def get_stk_setup(device: Device) -> str:
        """
        Get STK Setup Menu List with PDU Mode

        Corresponding command: AT+STSM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises SIMApplicationToolkitException:
        """
        raise NotImplementedError
