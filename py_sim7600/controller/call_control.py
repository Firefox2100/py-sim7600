"""
This file contains classes related to GPRS commands. This file may raise CallControlException,
remember to capture accordingly.
"""

from py_sim7600.device import Device
from py_sim7600.exceptions import CallControlException


class CallControl:
    """
    AT Commands for Call Control
    """

    def __init__(self, device: Device):
        self.device = device

    def control_voice_hangup(self, mode: int) -> bool:
        """
        Voice hang up control

        Corresponding command: AT+CVHU

        :param mode: The mode to set voice hang up to
        :return: True if successful
        :raises CallControlException: Mode parameter need to be 0 or 1
        """

        command = "AT+CVHU"

        if mode != 0 and mode != 1:
            raise CallControlException("Mode setting error")
        else:
            command += "=" + str(mode)

        self.device.send(
            command=command,
            back="OK",
        )

        return True

    def check_control_voice_hangup(self) -> bool:
        """
        Check voice hang up control

        Corresponding command: AT+CVHU

        :return: True if ATH or “drop DTR” shall cause a voice connection to be disconnected
        """

        command = "AT+CVHU?"

        result = self.device.send(
            command=command,
            back="OK",
        )

        return "1" in result

    @staticmethod
    def hang_up(device: Device) -> str:
        """
        Hang up call

        Corresponding command: AT+CHUP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def bearer_type(device: Device) -> str:
        """
        Select bearer service type

        Corresponding command: AT+CBST

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def radio_link(device: Device) -> str:
        """
        Radio link protocol

        Corresponding command: AT+CRLP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def service_report(device: Device) -> str:
        """
        Service reporting control

        Corresponding command: AT+CR

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def result_code(device: Device) -> str:
        """
        Cellular result codes

        Corresponding command: AT+CRC

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def list_call(device: Device) -> str:
        """
        List current calls

        Corresponding command: AT+CLCC

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def extended_error(device: Device) -> str:
        """
        Extended error report

        Corresponding command: AT+CEER

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def call_waiting(device: Device) -> str:
        """
        Call waiting

        Corresponding command: AT+CCWA

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def supplementary(device: Device) -> str:
        """
        Call related supplementary services

        Corresponding command: AT+CHLD

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def forward_control(device: Device) -> str:
        """
        Call forwarding number and conditions

        Corresponding command: AT+CCFC

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def calling_presentation(device: Device) -> str:
        """
        Calling line identification presentation

        Corresponding command: AT+CLIP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def calling_restriction(device: Device) -> str:
        """
        Calling line identification restriction

        Corresponding command: AT+CLIR

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def connected_presentation(device: Device) -> str:
        """
        Connected line identification presentation

        Corresponding command: AT+COLP

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def tone_generate(device: Device) -> str:
        """
        DTMF and tone generation

        Corresponding command: AT+VTS

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def tone_duration(device: Device) -> str:
        """
        Tone duration

        Corresponding command: AT+VTD

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def address_select(device: Device) -> str:
        """
        Select type of address

        Corresponding command: AT+CSTA

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def call_mode(device: Device) -> str:
        """
        Call mode

        Corresponding command: AT+CMOD

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def mute_speaker(device: Device) -> str:
        """
        Speaker mute control

        Corresponding command: AT+VMUTE

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def mute_microphone(device: Device) -> str:
        """
        Microphone mute control

        Corresponding command: AT+CMUT

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def mo_ring_urc_config(device: Device) -> str:
        """
        Enable or disable report MO ring URC

        Corresponding command: AT+MORING

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def speaker_volume(device: Device) -> str:
        """
        Loudspeaker volume level

        Corresponding command: AT+CLVL

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def set_sidetone(device: Device) -> str:
        """
        Set sidetone

        Corresponding command: AT+SIDET

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def change_acdb(device: Device) -> str:
        """
        Change default ACDB filename

        Corresponding command: AT+CACDBFN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def usb_audio(device: Device) -> str:
        """
        USB audio control

        Corresponding command: AT+CPCMREG

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def mic_gain(device: Device) -> str:
        """
        Adjust mic gain

        Corresponding command: AT+CMICGAIN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def out_gain(device: Device) -> str:
        """
        Adjust out gain

        Corresponding command: AT+COUTGAIN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def tx_volume(device: Device) -> str:
        """
        Adjust TX voice mic volume

        Corresponding command: AT+CTXVOL

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def tx_gain(device: Device) -> str:
        """
        Adjust TX voice mic gain

        Corresponding command: AT+CTXMICGAIN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def rx_volume(device: Device) -> str:
        """
        Adjust RX voice output speaker volume

        Corresponding command: AT+CRXVOL

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def farend_echo(device: Device) -> str:
        """
        Inhibit far-end echo

        Corresponding command: AT+CECH

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def doubletalk_echo(device: Device) -> str:
        """
        Inhibit echo during doubletalk

        Corresponding command: AT+CECDT

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def mic_noise_estimation(device: Device) -> str:
        """
        MIC NOISE suppression

        Corresponding command: AT+CNSN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def mic_noise_maximum(device: Device) -> str:
        """
        MIC NOISE suppression

        Corresponding command: AT+CNSLIM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def fns_mode(device: Device) -> str:
        """
        Adjust parameter fnsMode of RX_VOICE_FNS

        Corresponding command: AT+CFNSMOD

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def fns_input_gain(device: Device) -> str:
        """
        Adjust parameter fnsInputGain of RX_VOICE_FNS

        Corresponding command: AT+CFNSIN

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def fns_target_ns(device: Device) -> str:
        """
        Adjust parameter fnsTargetNS of RX_VOICE_FNS

        Corresponding command: AT+CFNSLVL

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def voice_mod_enable(device: Device) -> str:
        """
        Enable or disable VOICE_MOD_ENABLE

        Corresponding command: AT+CECRX

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def nlpp_gain(device: Device) -> str:
        """
        Modify the NLPP_gain in DSP

        Corresponding command: AT+CNLPPG

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def nlpp_limit(device: Device) -> str:
        """
        Modify the NLPP_limit in DSP

        Corresponding command: AT+CNLPPL

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def echo_canceller(device: Device) -> str:
        """
        Adjust echo canceller

        Corresponding command: AT+CECM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def usb_sample_rate(device: Device) -> str:
        """
        Set usb audio sample rate to 16K bit

        Corresponding command: AT+CPCMFRM

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def play_tone(device: Device) -> str:
        """
        Play tone

        Corresponding command: AT+CPTONE

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def codec_control(device: Device) -> str:
        """
        Control codec by Host device or Module

        Corresponding command: AT+CODECCTL

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def pcm_sample_rate(device: Device) -> str:
        """
        Modify the sampling rate of the PCM

        Corresponding command: AT+CPCMBANDWIDTH

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    @staticmethod
    def voice_device(device: Device) -> str:
        """
        Switch voice channel device

        Corresponding command: AT+CSDVC

        :param device: A SIM7600 device instance
        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError
