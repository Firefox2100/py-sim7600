"""
This module contains the enums used in the library.
"""

from enum import Enum, auto


"""
The Enum classes in this section is for V.25 TER controller.
"""


class PhonebookStorage(Enum):
    """
    The phonebook storage location.
    """
    EMERGENCY = 'EN'            # Emergency numbers
    LAST_DIALED = 'LD'          # Last number dialed phonebook
    ME_DIALED = 'DC'            # ME dialed calls list
    ME_MISSED = 'MC'            # ME missed (unanswered received) calls list
    ME_RECEIVED = 'RC'          # ME received calls list
    MSISDN = 'ON'               # MSISDN list
    SIM_FIXED_DIALING = 'FD'    # SIM fixed dialing phonebook
    SIM_PHONEBOOK = 'SM'        # SIM phonebook
    UE_PHONEBOOK = 'ME'         # UE phonebook


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
    GSM = 'GSM'                 # GSM default alphabet; this setting causes XON /XOFF problems.
    IRA = 'IRA'                 # International reference alphabet
    UCS2 = 'UCS2'               # 16-bit universal multiple-octet coded character set


"""
The Enum classes in this section is for status controller.
"""


class PhoneFunctionalityLevel(Enum):
    """
    The phone functionality level.
    """
    MINIMUM = 0                 # minimum functionality
    FULL = 1                    # full functionality, online mode
    NO_RF = 4                   # disable phone both transmit and receive RF circuits
    FACTORY_TEST = 5            # Factory Test Mode
    RESET = 6                   # Reset
    OFFLINE = 7                 # Offline Mode


class RestrictedSIMCommand(Enum):
    """
    The commands used in restricted SIM access.
    """
    READ_BINARY = 176
    READ_RECORD = 178
    GET_RESPONSE = 192
    UPDATE_BINARY = 214
    UPDATE_RECORD = 220
    STATUS = 242
    RETRIEVE_DATA = 203
    SET_DATA = 219

    def to_sim_me(self):
        """
        Convert the command to the SIM-ME command type.
        """

        if self == RestrictedSIMCommand.READ_BINARY:
            return SIMMECommandType.READ_BINARY
        elif self == RestrictedSIMCommand.READ_RECORD:
            return SIMMECommandType.READ_RECORD
        elif self == RestrictedSIMCommand.GET_RESPONSE:
            return SIMMECommandType.GET_RESPONSE
        elif self == RestrictedSIMCommand.UPDATE_BINARY:
            return SIMMECommandType.UPDATE_BINARY
        elif self == RestrictedSIMCommand.UPDATE_RECORD:
            return SIMMECommandType.UPDATE_RECORD
        elif self == RestrictedSIMCommand.STATUS:
            return SIMMECommandType.STATUS
        elif self == RestrictedSIMCommand.RETRIEVE_DATA:
            return SIMMECommandType.FETCH
        elif self == RestrictedSIMCommand.SET_DATA:
            return SIMMECommandType.UPDATE_BINARY


class ElementaryFileID(Enum):
    """
    The ID of EF (Elementary data File) in SIM.
    """
    # EFs under MF
    ACCESS_RULE_REFERENCE_MF = 0x2F06
    EF_DIR = 0x2F00
    EXTENDED_LANGUAGE_PREFERENCES = 0x2F05
    ICCID = 0x2FE2

    # EFs under USIM ADF
    ACCESS_CONTROL_CLASS = 0x6F78
    ACCESS_POINT_NAME_CONTROL_LIST = 0x6F57
    ACCESS_RULE_REFERENCE_USIM = 0x6F06
    ACCUMULATED_CALL_METER = 0x6F39
    ACM_MAXIMUM_VALUE = 0x6F37
    ADMINISTRATIVE_DATA = 0x6FAD
    ADMINISTRATOR_ROOT_PUBLIC_KEY = 0x4F42
    AUTOMATIC_ANSWER_FOR_EMLPP_SERVICE = 0x6FB6
    BARRED_DIALING_NUMBERS_ADF = 0x6F4D
    C_AND_I_KEYS_FOR_PKT_SWITCHED_DOMAIN = 0x6F09
    CALL_FORWARDING_INDICATOR_STATUS = 0x6FCB
    CAPABILITY_CONFIG_PARAMETERS2 = 0x6F4F
    CELL_BCAST_MSG_ID_FOR_DATA_DOWNLOAD = 0x6F48
    CELL_BCAST_MSG_ID_RANGE_SELECTION = 0x6F50
    CELL_BCAST_MSG_IDENTIFIER_SELECTION = 0x6F45
    CHANGE_COUNTER_ADF = 0x4F23
    CIPHERING_AND_INTEGRITY_KEYS = 0x6F08
    COMPARISON_METHOD_INFORMATION_ADF = 0x6F58
    COOPERATIVE_NETWORK_LIST = 0x6F32
    CPBCCH_INFORMATION = 0x4F63
    CPHS_CALL_FORWARDING_FLAG = 0x6F13
    CPHS_CUSTOMER_SERVICE_PROFILE = 0x6F15
    CPHS_INFORMATION = 0x6F16
    CPHS_MAILBOX_NUMBER = 0x6F17
    CPHS_OPERATOR_NAME_STRING = 0x6F14
    CPHS_SERVICE_STRING_TABLE = 0x6F12
    CPHS_VOICE_MAIL_WAITING_INDICATOR = 0x6F11
    CUSTOMER_SERVICE_PROFILE_LINE2 = 0x6F98
    DE_PERSONALIZATION_CONTROL_KEYS = 0x6F2C
    DYNAMIC_FLAGS_STATUS = 0x6F9F
    DYNAMIC2_FLAG_SETTING = 0x6F92
    EF_PARAMS_WELCOME_MESSAGE = 0x6F9B
    EMERGENCY_CALL_CODES = 0x6FB7
    ENABLED_SERVICES_TABLE = 0x6F56
    ENH_MULTI_LEVEL_PRECEDENCE_AND_PRI = 0x6FB5
    EQUIVALENT_HPLMN = 0x6FD9
    EXTENSION2_ADF = 0x6F4B
    EXTENSION3_ADF = 0x6F4C
    EXTENSION4_ADF = 0x6F55
    EXTENSION5 = 0x6F4E
    EXTENSION6 = 0x6FC8
    EXTENSION8 = 0x6FCF
    FIXED_DIALING_NUMBERS_ADF = 0x6F3B
    FORBIDDEN_PLMNS = 0x6F7B
    GBA_BOOTSTRAPPING_PARAMETERS = 0x6FD6
    GBA_NAF_LIST = 0x6FDA
    GPRS_CIPHERING_KEY = 0x4F52
    GROUP_IDENTIFIER_LEVEL = 0x6F3E
    GROUP_IDENTIFIER_LEVEL2 = 0x6F3F
    GROUP_IDENTITY = 0x6FC2
    GSM_CIPHERING_KEY_KC = 0x4F20
    IMSI = 0x6F07
    HPLMN_SEARCH_PERIOD = 0x6F31
    HPLMN_SELECTOR_WITH_ACCESS_TECHNOLOGY = 0x6F62
    HYPERFRAME_NUMBER = 0x6F5B
    INCOMING_CALL_INFORMATION = 0x6F80
    INCOMING_CALL_TIMER = 0x6F82
    INVESTIGATION_SCAN = 0x4F64
    KEY_FOR_HIDDEN_PHONEBOOK_ENTRIES = 0x6FC3
    LANGUAGE_INDICATION = 0x6F05
    LOCATION_INFORMATION = 0x6F7E
    MAILBOX_DIALING_NUMBER = 0x6FC7
    MAILBOX_IDENTIFIER = 0x6FC9
    MAXIMUM_VALUE_OF_HYPERFRAME_NUMBER = 0x6F5C
    MBMS_SERVICE_KEY = 0x6FD7
    MBMS_USER_KEY = 0x6FD8
    MESSAGE_WAITING_INDICATION_STATUS = 0x6FCA
    MEXE_SERVICE_TABLE = 0x4F40
    MMS_ISSUER_CONNECTIVITY_PARAMETERS = 0x6FD0
    MMS_NOTIFICATION = 0x6FCE
    MMS_USER_CONNECTIVITY_PARAMETERS = 0x6FD2
    MMS_USER_PREFERENCES = 0x6FD1
    MSISDN_ADF = 0x6F40
    NETWORK_PARAMETERS = 0x6FC4
    OBJECT_DIRECTORY_FILE = 0x5031
    OPERATOR_PLMN_LIST = 0x6FC6
    OPERATOR_ROOT_PUBLIC_KEY = 0x4F41
    OPLMN_SELECTOR = 0x6F5D
    OPLMN_SELECTOR_WITH_ACCESS_TECH = 0x6F61
    OUTGOING_CALL_INFORMATION = 0x6F81
    OUTGOING_CALL_TIMER = 0x6F83
    PACKET_SWITCHED_LOCATION_INFORMATION = 0x6F73
    PHONE_BOOK_REFERENCE_FILE_ADF = 0x4F30
    PHONE_BOOK_SYNCHRONIZATION_CENTER_ADF = 0x4F22
    PLMN_NETWORK_NAME = 0x6FC5
    PREVIOUS_UNIQUE_IDENTIFIER_ADF = 0x4F24
    PRICE_PER_UNIT_AND_CURRENCY_TABLE = 0x6F41
    RPLMN_LAST_USED_ACCESS_TECH = 0x6F65
    SERVICE_DIALING_NUMBERS_ADF = 0x6F49
    SERVICE_PROVIDER_DISPLAY_INFORMATION = 0x6FCD
    SERVICE_PROVIDER_NAME = 0x6F46
    SHORT_MESSAGES_ADF = 0x6F3C
    SMS_PARAMETERS_ADF = 0x6F42
    SMS_REPORTS_ADF = 0x6F47
    SMS_STATUS_ADF = 0x6F43
    THIRD_PARTY_ROOT_PUBLIC_KEY = 0x4F43
    TOKEN_INFORMATION_FILE = 0x5032
    UIM_USIM_SPT_TABLE = 0x6FD2
    UNUSED_SPACE_INFORMATION_FILE = 0x5033
    USER_CONTROLLED_PLMN_SELECTOR = 0x6F30
    USER_CONTROLLED_PLMN_SELECTOR_W_ACC_TECH = 0x6F60
    USIM_SERVICE_TABLE = 0x6F38

    # EFs under Telecom DF
    ABBREVIATED_DIALING_NUMBERS = 0x6F3A
    ACCESS_RULE_REFERENCE = 0x6F06
    BARRED_DIALING_NUMBERS_TDF = 0x6F4D
    CAPABILITY_CONFIGURATION_PARAMETERS = 0x6F3D
    CHANGE_COUNTER_TDF = 0x4F23
    COMPARISON_METHOD_INFORMATION_TDF = 0x6F58
    EXTENDED_CCP = 0x6F4F
    EXTENSION1 = 0x6F4A
    EXTENSION2_TDF = 0x6F4B
    EXTENSION3_TDF = 0x6F4C
    EXTENSION4_TDF = 0x6F4D
    FIXED_DIALING_NUMBERS_TDF = 0x6F3B
    IMAGE = 0x4F20
    LAST_NUMBER_DIALED = 0x6F44
    MSISDN_TDF = 0x6F40
    PHONE_BOOK_REFERENCE_FILE_TDF = 0x4F30
    PHONE_BOOK_SYNCHRONIZATION_CENTER_TDF = 0x4F22
    PREVIOUS_UNIQUE_IDENTIFIER_TDF = 0x4F24
    SERVICE_DIALING_NUMBERS_TDF = 0x6F49
    SETUP_MENU_ELEMENTS = 0x6F54
    SHORT_MESSAGES_TDF = 0x6F3C
    SMS_PARAMETERS_TDF = 0x6F42
    SMS_REPORTS_TDF = 0x6F47
    SMS_STATUS_TDF = 0x6F43


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


class CallState(Enum):
    """
    The state of a call.
    """
    ACTIVE = 0
    HELD = 1
    DIALING = 2
    ALERTING = 3
    INCOMING = 4
    WAITING = 5
    DISCONNECT = 6


class BearerServiceMode(Enum):
    """
    The mode of bearer service in a data call.
    """
    VOICE = 0
    DATA = 1
    FAX = 2
    UNKNOWN = 9


class CallNumberType(Enum):
    """
    The type of the phone number in a call.
    """
    RESTRICTED = 128
    INTERNATIONAL = 145
    NATIONAL = 161
    NETWORK_SPECIFIC = 177
    OTHER = 129


"""
The Enum classes in this section is for SIM-ME interface model.
"""


class SIMMECommandType(Enum):
    """
    The SIM-ME command type.
    """
    SELECT = auto()
    STATUS = auto()
    READ_BINARY = auto()
    UPDATE_BINARY = auto()
    READ_RECORD = auto()
    UPDATE_RECORD = auto()
    SEEK = auto()
    INCREASE = auto()
    VERIFY_CHV = auto()
    CHANGE_CHV = auto()
    DISABLE_CHV = auto()
    ENABLE_CHV = auto()
    UNBLOCK_CHV = auto()
    INVALIDATE = auto()
    REHABILITATE = auto()
    RUN_GSM_ALGORITHM = auto()
    SLEEP = auto()
    GET_RESPONSE = auto()
    TERMINAL_PROFILE = auto()
    ENVELOPE = auto()
    FETCH = auto()
    TERMINAL_RESPONSE = auto()
