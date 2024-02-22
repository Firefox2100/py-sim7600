"""
This file contains classes related to GPRS commands. This file may raise CallControlException,
remember to capture accordingly.
"""

import re

from py_sim7600.controller import DeviceController
from py_sim7600.exceptions import CallControlException, DeviceException
from py_sim7600.model.enums import BearerServiceSpeed, BearerServiceName, BearerServiceConnectionElement
from py_sim7600.model.call import Call


class CallController(DeviceController):
    """
    AT Commands for Call Control
    """

    def set_control_voice_hangup(self, disconnect_ath: bool) -> bool:
        """
        Voice hang up control

        Corresponding command: AT+CVHU

        :param disconnect_ath: ATH or “drop DTR” shall cause a voice connection to be disconnected
        :return: True if successful
        :rtype: bool
        :raises CallControlException: Mode parameter need to be 0 or 1
        """

        command = 'AT+CVHU='

        if disconnect_ath:
            command += '0'
        else:
            command += '1'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting control voice hangup: {e}')

        return True

    def get_control_voice_hangup(self) -> bool:
        """
        Check voice hang up control

        Corresponding command: AT+CVHU

        :return: True if ATH or “drop DTR” shall cause a voice connection to be disconnected
        :rtype: bool
        """

        command = 'AT+CVHU?'

        try:
            result = self.device.send(
                command=command,
                back='OK',
            )
        except DeviceException as e:
            raise CallControlException(f'Error checking control voice hangup: {e}')

        return '0' in result

    def hang_up(self) -> int:
        """
        Hang up call

        Corresponding command: AT+CHUP

        :return: Length of the call in seconds; 0 if no call is in progress
        :rtype: int
        """

        command = 'AT+CHUP'

        try:
            result = self.device.send(
                command=command,
                back='OK',
            )
        except DeviceException as e:
            raise CallControlException(f'Error hanging up call: {e}')

        pattern = r'VOICE CALL:END: (\d{2})(\d{2})(\d{2})'
        matches = re.search(pattern, result)

        if matches:
            return int(matches.group(1)) * 3600 + int(matches.group(2)) * 60 + int(matches.group(3))

        return 0

    def set_bearer_type(self,
                        bearer_speed: BearerServiceSpeed,
                        bearer_name: BearerServiceName,
                        bearer_ce: BearerServiceConnectionElement,
                        ) -> bool:
        """
        Select bearer service type

        Corresponding command: AT+CBST

        :param bearer_speed: The speed for bearer service in a data call
        :param bearer_name: The type of bearer service in a data call
        :param bearer_ce: The connection element for bearer service in a data call
        :return: True if successful
        :rtype: bool
        :raises CallControlException: Bearer name and connection element setting error
        """

        command = 'AT+CBST='

        if bearer_speed == BearerServiceSpeed.BIT_TRANSPARENT or bearer_speed == BearerServiceSpeed.MULTIMEDIA:
            # For bit-transparent and multimedia, bearer_name and bearer_ce are fixed
            if bearer_name != BearerServiceName.SYNC_MODEM or bearer_ce != BearerServiceConnectionElement.TRANSPARENT:
                raise CallControlException('Bearer name and connection element setting error')

        command += f'{bearer_speed.value},{bearer_name.value},{bearer_ce.value}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting bearer type: {e}')

        return True

    def get_bearer_type(self) -> tuple[BearerServiceSpeed, BearerServiceName, BearerServiceConnectionElement]:
        """
        Read selected bearer service type

        Corresponding command: AT+CBST

        :return: The speed for bearer service in a data call, the type of bearer service in a data call,
                 and the connection element for bearer service in a data call as a tuple
        :rtype: tuple[BearerServiceSpeed, BearerServiceName, BearerServiceConnectionElement]
        """

        command = 'AT+CBST?'

        try:
            result = self.device.send(
                command=command,
                back='OK',
            )
        except DeviceException as e:
            raise CallControlException(f'Error checking bearer type: {e}')

        pattern = r'\+CBST: (\d+),(\d+),(\d+)'

        matches = re.search(pattern, result)

        if matches:
            return (
                BearerServiceSpeed(int(matches.group(1))),
                BearerServiceName(int(matches.group(2))),
                BearerServiceConnectionElement(int(matches.group(3))),
            )

    def set_rlp_parameter(self,
                          rlp_version: int = 1,
                          iws: int = None,
                          mws: int = None,
                          ack_timer: int = None,
                          retry_times: int = None,
                          re_sequence_timer: int = None,
                          ) -> bool:
        """
        Radio link protocol

        Corresponding command: AT+CRLP

        :param rlp_version: RLP version number in integer format, and it can be 0, 1 or 2
        :param iws: IWF to MS window size
        :param mws: MS to IWF window size
        :param ack_timer: Acknowledgement timer, in 10ms unit
        :param retry_times: Maximum number of retransmissions
        :param re_sequence_timer: Re-sequencing timer, in 10ms unit
        :return: True if setting successful
        :rtype: bool
        :raises CallControlException: RLP version number need to be 0, 1 or 2
        """

        if rlp_version not in [0, 1, 2]:
            raise CallControlException('RLP version number need to be 0, 1 or 2')

        command = 'AT+CRLP='

        if iws is not None:
            command += f'{iws}'
            if mws is not None:
                command += f',{mws}'
                if ack_timer is not None:
                    command += f',{ack_timer}'
                    if retry_times is not None:
                        command += f',{retry_times}'
                        if rlp_version is not None:
                            command += f',{rlp_version}'
                            if re_sequence_timer is not None:
                                command += f',{re_sequence_timer}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting RLP parameter: {e}')

        return True

    def get_rlp_parameter(self) -> list[tuple[int, ...]]:
        """
        Read RLP parameter

        Corresponding command: AT+CRLP

        :return: RLP version number, IWF to MS window size, MS to IWF window size, Acknowledgement timer,
                 Maximum number of retransmissions, and Re-sequencing timer as a tuple
        :rtype: tuple[int, ...]
        """

        command = 'AT+CRLP?'

        try:
            result = self.device.send(
                command=command,
                back='OK',
            )
        except DeviceException as e:
            raise CallControlException(f'Error checking RLP parameter: {e}')

        pattern = r'\+CRLP: [\d,]+'
        matches = re.findall(pattern, result)

        parameters = []

        for match in matches:
            values = match.split(': ')[1].split(',')
            parameters.append(tuple(int(value) for value in values))

        return parameters

    def set_service_report(self, report=False) -> bool:
        """
        Set service reporting control

        Corresponding command: AT+CR

        :param report: Enable or disable intermediate result code presentation
        :return: True if successful
        :rtype: bool
        """

        command = f'AT+CR={int(report)}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting service reporting: {e}')

        return True

    def get_service_report(self) -> bool:
        """
        Get service reporting control status

        Corresponding command: AT+CR

        :return: Whether intermediate result code presentation is enabled
        :rtype: bool
        """

        command = 'AT+CR?'

        try:
            result = self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting service reporting: {e}')

        return '1' in result

    def set_result_code(self, extended_format=False) -> bool:
        """
        Cellular result codes

        Corresponding command: AT+CRC

        :param extended_format: Enable or disable extended format of incoming call indication
        :return: True if successful
        :rtype: bool
        """

        command = f'AT+CRC={int(extended_format)}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting result code: {e}')

        return True

    def get_result_code(self) -> bool:
        """
        Get cellular result codes status

        Corresponding command: AT+CRC

        :return: Whether extended format of incoming call indication is enabled
        :rtype: bool
        """

        command = 'AT+CRC?'

        try:
            result = self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting result code: {e}')

        return '1' in result

    def set_list_call(self, auto_report=False) -> bool:
        """
        Set auto list current calls

        Corresponding command: AT+CLCC

        :param auto_report: Enable or disable automatic report of current calls when call status changes
        :return: True if successful
        :rtype: bool
        """

        command = f'AT+CLCC={int(auto_report)}'

        try:
            self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting list call: {e}')

        return True

    def get_list_call(self) -> bool:
        """
        Get auto list current calls status

        Corresponding command: AT+CLCC

        :return: Whether automatic report of current calls when call status changes is enabled
        :rtype: bool
        """

        command = 'AT+CLCC?'

        try:
            result = self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error setting list call: {e}')

        return '1' in result

    def list_call(self) -> list[Call]:
        """
        List all current calls

        Corresponding command: AT+CLCC

        :return:
        """

        command = 'AT+CLCC'

        try:
            result = self.device.send(
                command=command,
                back='OK',
                error_pattern=['ERROR']
            )
        except DeviceException as e:
            raise CallControlException(f'Error listing calls: {e}')

        calls = []

        pattern = r'\+CLCC: [\w,]+'
        matches = re.findall(pattern, result)

        for match in matches:
            calls.append(Call.from_list_call(match))

        return calls

    def extended_error(self) -> str:
        """
        Extended error report

        Corresponding command: AT+CEER

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def call_waiting(self) -> str:
        """
        Call waiting

        Corresponding command: AT+CCWA

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def supplementary(self) -> str:
        """
        Call related supplementary services

        Corresponding command: AT+CHLD

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def forward_control(self) -> str:
        """
        Call forwarding number and conditions

        Corresponding command: AT+CCFC

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def calling_presentation(self) -> str:
        """
        Calling line identification presentation

        Corresponding command: AT+CLIP

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def calling_restriction(self) -> str:
        """
        Calling line identification restriction

        Corresponding command: AT+CLIR

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def connected_presentation(self) -> str:
        """
        Connected line identification presentation

        Corresponding command: AT+COLP

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def tone_generate(self) -> str:
        """
        DTMF and tone generation

        Corresponding command: AT+VTS

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def tone_duration(self) -> str:
        """
        Tone duration

        Corresponding command: AT+VTD

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def address_select(self) -> str:
        """
        Select type of address

        Corresponding command: AT+CSTA

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def call_mode(self) -> str:
        """
        Call mode

        Corresponding command: AT+CMOD

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def mute_speaker(self) -> str:
        """
        Speaker mute control

        Corresponding command: AT+VMUTE

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def mute_microphone(self) -> str:
        """
        Microphone mute control

        Corresponding command: AT+CMUT

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def mo_ring_urc_config(self) -> str:
        """
        Enable or disable report MO ring URC

        Corresponding command: AT+MORING

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def speaker_volume(self) -> str:
        """
        Loudspeaker volume level

        Corresponding command: AT+CLVL

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def set_sidetone(self) -> str:
        """
        Set sidetone

        Corresponding command: AT+SIDET

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def change_acdb(self) -> str:
        """
        Change default ACDB filename

        Corresponding command: AT+CACDBFN

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def usb_audio(self) -> str:
        """
        USB audio control

        Corresponding command: AT+CPCMREG

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def mic_gain(self) -> str:
        """
        Adjust mic gain

        Corresponding command: AT+CMICGAIN

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def out_gain(self) -> str:
        """
        Adjust out gain

        Corresponding command: AT+COUTGAIN

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def tx_volume(self) -> str:
        """
        Adjust TX voice mic volume

        Corresponding command: AT+CTXVOL

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def tx_gain(self) -> str:
        """
        Adjust TX voice mic gain

        Corresponding command: AT+CTXMICGAIN

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def rx_volume(self) -> str:
        """
        Adjust RX voice output speaker volume

        Corresponding command: AT+CRXVOL

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def farend_echo(self) -> str:
        """
        Inhibit far-end echo

        Corresponding command: AT+CECH

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def doubletalk_echo(self) -> str:
        """
        Inhibit echo during doubletalk

        Corresponding command: AT+CECDT

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def mic_noise_estimation(self) -> str:
        """
        MIC NOISE suppression

        Corresponding command: AT+CNSN

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def mic_noise_maximum(self) -> str:
        """
        MIC NOISE suppression

        Corresponding command: AT+CNSLIM

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def fns_mode(self) -> str:
        """
        Adjust parameter fnsMode of RX_VOICE_FNS

        Corresponding command: AT+CFNSMOD

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def fns_input_gain(self) -> str:
        """
        Adjust parameter fnsInputGain of RX_VOICE_FNS

        Corresponding command: AT+CFNSIN

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def fns_target_ns(self) -> str:
        """
        Adjust parameter fnsTargetNS of RX_VOICE_FNS

        Corresponding command: AT+CFNSLVL

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def voice_mod_enable(self) -> str:
        """
        Enable or disable VOICE_MOD_ENABLE

        Corresponding command: AT+CECRX

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def nlpp_gain(self) -> str:
        """
        Modify the NLPP_gain in DSP

        Corresponding command: AT+CNLPPG

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def nlpp_limit(self) -> str:
        """
        Modify the NLPP_limit in DSP

        Corresponding command: AT+CNLPPL

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def echo_canceller(self) -> str:
        """
        Adjust echo canceller

        Corresponding command: AT+CECM

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def usb_sample_rate(self) -> str:
        """
        Set usb audio sample rate to 16K bit

        Corresponding command: AT+CPCMFRM

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def play_tone(self) -> str:
        """
        Play tone

        Corresponding command: AT+CPTONE

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def codec_control(self) -> str:
        """
        Control codec by Host device or Module

        Corresponding command: AT+CODECCTL

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def pcm_sample_rate(self) -> str:
        """
        Modify the sampling rate of the PCM

        Corresponding command: AT+CPCMBANDWIDTH

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError

    def voice_device(self) -> str:
        """
        Switch voice channel device

        Corresponding command: AT+CSDVC

        :return: Results from device return buffer
        :raises CallControlException:
        """
        raise NotImplementedError
