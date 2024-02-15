"""
This module contains the enums used in the library.
"""

from enum import Enum


"""
The Enum classes in this section is for V.25 TER controller.
"""


class PhonebookStorage(Enum):
    """
    The phonebook storage location.
    """
    ME_DIALED = 'DC'            # ME dialed calls list
    ME_MISSED = 'MC'            # ME missed (unanswered received) calls list
    ME_RECEIVED = 'RC'          # ME received calls list
    SIM_PHONEBOOK = 'SM'        # SIM phonebook
    UE_PHONEBOOK = 'ME'         # UE phonebook
    SIM_FIXED_DIALING = 'FD'    # SIM fixed dialing phonebook
    MSISDN = 'ON'               # MSISDN list
    LAST_DIALED = 'LD'          # Last number dialed phonebook
    EMERGENCY = 'EN'            # Emergency numbers


class ControlCharacterFormat(Enum):
    """
    The control character framing format for serial port communication.
    """
    D8S2 = 1                    # 8 data bits, 2 stop bits
    D8P1S1 = 2                  # 8 data bits, 1 parity bit, 1 stop bit
    D8S1 = 3                    # 8 data bits, 1 stop bit
    D7S2 = 4                    # 7 data bits, 2 stop bits
    D7P1S1 = 5                  # 7 data bits, 1 parity bit, 1 stop bit
    D7S1 = 6                    # 7 data bits, 1 stop bit
    

class ControlCharacterParity(Enum):
    """
    The control character parity for serial port communication.
    """
    ODD = 0                     # Odd parity
    EVEN = 1                    # Even parity
    SPACE = 2                   # Space parity
    NONE = 3                    # No parity


class TECharacterSet(Enum):
    """
    The character set for TE.
    """
    GSM = 'GSM'                # GSM default alphabet; this setting causes XON /XOFF problems.
    IRA = 'IRA'                # International reference alphabet
    UCS2 = 'UCS2'              # 16-bit universal multiple-octet coded character set


"""
The Enum classes in this section is for call controller.
"""


class BearerServiceSpeed(Enum):
    """
    The speed for bearer service in a data call.
    """
    AUTO = 0                # autobauding
    V32 = 7                 # 9600 bps (V.32)
    V34_9600 = 12           # 9600 bps (V.34)
    V34_14400 = 14          # 14400 bps(V.34)
    V34_28800 = 16          # 28800 bps(V.34)
    V34_33600 = 17          # 33600 bps(V.34)
    V120_9600 = 39          # 9600 bps(V.120)
    V120_14400 = 43         # 14400 bps(V.120)
    V120_28800 = 48         # 28800 bps(V.120)
    V120_56000 = 51         # 56000 bps(V.120)
    V110_9600 = 71          # 9600 bps(V.110)
    V110_14400 = 75         # 14400 bps(V.110)
    V110_28800 = 80         # 28800 bps(V.110 or X.31 flag stuffing)
    V110_38400 = 81         # 38400 bps(V.110 or X.31 flag stuffing)
    V110_56000 = 83         # 56000 bps(V.110 or X.31 flag stuffing)
    X31_64000 = 84          # 64000 bps(X.31 flag stuffing)
    BIT_TRANSPARENT = 116   # 64000 bps(bit transparent)
    MULTIMEDIA = 134        # 64000 bps(multimedia)


class BearerServiceName(Enum):
    """
    The type of bearer service in a data call.
    """
    ASYNC_MODEM = 0         # Asynchronous modem
    SYNC_MODEM = 1          # Synchronous modem
    RDI = 4                 # data circuit asynchronous (RDI)


class BearerServiceConnectionElement(Enum):
    """
    The connection element for bearer service in a data call.
    """
    TRANSPARENT = 0         # Transparent
    NON_TRANSPARENT = 1     # Non-transparent
