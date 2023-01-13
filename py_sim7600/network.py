"""
This file contains classes related to network commands. This file may raise NetworkException,
remember to capture accordingly.
"""

from py_sim7600.device import Device
from py_sim7600.error import NetworkException


class Network:
    """
    AT Commands for Network
    """

    @staticmethod
    def register(device: Device) -> str:
        """
        Network Registration

        Corresponding command: AT+CREG

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError
    
    @staticmethod
    def select_operator(device: Device) -> str:
        """
        Operator selection

        Corresponding command: AT+COPS

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError
    
    @staticmethod
    def facility_lock(device: Device) -> str:
        """
        Facility lock

        Corresponding command: AT+CLCK

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError
    
    @staticmethod
    def change_password(device: Device) -> str:
        """
        Change password

        Corresponding command: AT+CPWD

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def cug(device: Device) -> str:
        """
        Closed User Group

        Corresponding command: AT+CCUG

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def uss_data(device: Device) -> str:
        """
        Unstructured supplementary service data

        Corresponding command: AT+CUSD

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def advice_of_charge(device: Device) -> str:
        """
        Advice of Charge

        Corresponding command: AT+CAOC

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def supplementary_notification(device: Device) -> str:
        """
        Supplementary service notifications

        Corresponding command: AT+CSSN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def operator_preference(device: Device) -> str:
        """
        Preferred operator list

        Corresponding command: AT+CPOL

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def operator_name(device: Device) -> str:
        """
        Read operator names

        Corresponding command: AT+COPN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def mode_preference(device: Device) -> str:
        """
        Preferred mode selection

        Corresponding command: AT+CNMP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def band_preference(device: Device) -> str:
        """
        Preferred band selection

        Corresponding command: AT+CNBP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def acquisitions_preference(device: Device) -> str:
        """
        Acquisitions order preference

        Corresponding command: AT+CNAOP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def ue_info(device: Device) -> str:
        """
        Inquiring UE system information

        Corresponding command: AT+CPSI

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def network_system(device: Device) -> str:
        """
        Show network system mode

        Corresponding command: AT+CNSMOD

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def eps_status(device: Device) -> str:
        """
        EPS network registration status

        Corresponding command: AT+CEREG

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def auto_time(device: Device) -> str:
        """
        Automatic time and time zone update

        Corresponding command: AT+CTZU

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError

    @staticmethod
    def time_report(device: Device) -> str:
        """
        Time and time zone reporting

        Corresponding command: AT+CTZR

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises NetworkException:
        """
        raise NotImplementedError
