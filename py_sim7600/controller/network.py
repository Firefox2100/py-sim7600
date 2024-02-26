"""
This file contains classes related to network commands.

This file may raise NetworkException,
remember to capture accordingly.
"""

from py_sim7600.controller import DeviceController
from py_sim7600.exceptions import NetworkException
from py_sim7600.model import enums


class NetworkController(DeviceController):
    """
    AT Commands for Network
    """

    def register(self) -> str:
        """
        Network Registration

        Corresponding command: AT+CREG

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def select_operator(self) -> str:
        """
        Operator selection

        Corresponding command: AT+COPS

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError
    
    def facility_lock(self) -> str:
        """
        Facility lock

        Corresponding command: AT+CLCK

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError
    
    def change_password(self) -> str:
        """
        Change password

        Corresponding command: AT+CPWD

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def cug(self) -> str:
        """
        Closed User Group

        Corresponding command: AT+CCUG

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def uss_data(self) -> str:
        """
        Unstructured supplementary service data

        Corresponding command: AT+CUSD

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def advice_of_charge(self) -> str:
        """
        Advice of Charge

        Corresponding command: AT+CAOC

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def supplementary_notification(self) -> str:
        """
        Supplementary service notifications

        Corresponding command: AT+CSSN

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def operator_preference(self) -> str:
        """
        Preferred operator list

        Corresponding command: AT+CPOL

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def operator_name(self) -> str:
        """
        Read operator names

        Corresponding command: AT+COPN

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def mode_preference(self) -> str:
        """
        Preferred mode selection

        Corresponding command: AT+CNMP

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def band_preference(self) -> str:
        """
        Preferred band selection

        Corresponding command: AT+CNBP

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def acquisitions_preference(self) -> str:
        """
        Acquisitions order preference

        Corresponding command: AT+CNAOP

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def ue_info(self) -> str:
        """
        Inquiring UE system information

        Corresponding command: AT+CPSI

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def network_system(self) -> str:
        """
        Show network system mode

        Corresponding command: AT+CNSMOD

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def eps_status(self) -> str:
        """
        EPS network registration status

        Corresponding command: AT+CEREG

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def auto_time(self) -> str:
        """
        Automatic time and time zone update

        Corresponding command: AT+CTZU

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    def time_report(self) -> str:
        """
        Time and time zone reporting

        Corresponding command: AT+CTZR

        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

