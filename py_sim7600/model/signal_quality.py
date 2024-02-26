import re
from functools import total_ordering


@total_ordering
class SignalQuality:
    """
    This class represents the signal quality of the device.
    """
    def __init__(self,
                 strength: int,
                 is_rscp: bool,
                 bit_error_rate: int,
                 ):
        """
        This class represents the signal quality of the device.

        :param strength: The strength of the signal, in dBm.
        :param is_rscp: Whether the strength is RSCP (using TD-SCDMA) or RSSI (using GSM).
        :param bit_error_rate: The bit error rate of the signal, in category.
        """

        self.strength = strength
        self.is_rscp = is_rscp
        self.bit_error_rate = bit_error_rate

    def __eq__(self, other: 'SignalQuality') -> bool:
        return (self.strength == other.strength
                and self.is_rscp == other.is_rscp
                and self.bit_error_rate == other.bit_error_rate)

    def __lt__(self, other: 'SignalQuality') -> bool:
        # Different signal types are not comparable
        if self.is_rscp != other.is_rscp:
            raise TypeError('Cannot compare RSCP and RSSI signal quality')

        # The one with undefined strength or BER is always worse
        if self.strength == -999 or self.bit_error_rate == 99:
            return True
        if other.strength == -999 or other.bit_error_rate == 99:
            return False

        # If strength is the same, compare BER
        if self.strength == other.strength:
            return self.bit_error_rate > other.bit_error_rate

        # Strength takes precedence
        return self.strength < other.strength

    @classmethod
    def from_quality_query(cls, response: str) -> 'SignalQuality':
        """
        Creates a SignalQuality object from a quality query response (+CSQ).

        :param response: The response to the quality query.
        :return: A SignalQuality object.
        :rtype: SignalQuality
        :raises ValueError: If the response is invalid.
        """

        pattern = r'\+CSQ: (\d+),(\d+)'
        match = re.search(pattern, response)

        if not match:
            raise ValueError('Invalid response')

        is_rscp = False

        rssi = int(match.group(1))

        if rssi <= 31:
            strength = -113 + 2 * rssi
        elif rssi < 99:
            strength = -51
        elif rssi == 99:
            strength = -999
        else:
            # Above 100, it's RSCP
            is_rscp = True

            if rssi <= 191:
                strength = rssi - 216
            elif rssi < 199:
                strength = -26
            elif rssi == 199:
                strength = -999
            else:
                raise ValueError('Invalid RSCP value')

        bit_error_rate = int(match.group(2))

        if bit_error_rate < 0 or (bit_error_rate > 7 and bit_error_rate != 99):
            raise ValueError('Invalid bit error rate value')

        return cls(strength, is_rscp, bit_error_rate)

    @property
    def ber_max(self) -> float:
        """
        The maximum bit error rate.
        """

        if self.bit_error_rate == 0:
            return 0.0001
        elif self.bit_error_rate == 1:
            return 0.001
        elif self.bit_error_rate == 2:
            return 0.005
        elif self.bit_error_rate == 3:
            return 0.01
        elif self.bit_error_rate == 4:
            return 0.02
        elif self.bit_error_rate == 5:
            return 0.04
        elif self.bit_error_rate == 6:
            return 0.08
        elif self.bit_error_rate == 7:
            return 1
        else:
            return 1
