"""
This file contains classes related to phonebook commands. This file may raise GPRSException,
remember to capture accordingly.
"""

from py_sim7600.device import Device
from py_sim7600.exceptions import GPRSException


class Phonebook:
    """
    AT Commands for Phonebook
    """

    @staticmethod
    def select_memory(device: Device) -> str:
        """
        Select Phonebook memory storage

        Corresponding command: AT+CPBS

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises GPRSException:
        """
        pass


"""
AT+CGREG GPRS network registration status
AT+CGATT Packet domain attach or detach
AT+CGACT GPRS network registration status
AT+CGDCONT Define PDP context
AT+CGDSCONT Define Secondary PDP Context
AT+CGTFT Traffic Flow Template
AT+CGQREQ Quality of service profile (requested)
AT+CGEQREQ 3G quality of service profile (requested)
AT+CGQMIN Quality of service profile (minimum acceptable)
AT+CGEQMIN 3G quality of service profile (minimum acceptable)
AT+CGDATA Enter data state
AT+CGPADDR Show PDP address
AT+CGCLASS GPRS mobile station class
AT+CGEREP GPRS event reporting
AT+CGAUTH Set type of authentication for PDP-IP connections of GPRS
"""
