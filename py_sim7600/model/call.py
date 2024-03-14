import re

from .enums import CallState, CallNumberType, BearerServiceMode


class Call:
    """
    This class represents a call object.
    """
    def __init__(self,
                 call_id: int,
                 oriented: bool,
                 state: CallState,
                 service_mode: BearerServiceMode,
                 multiparty: bool,
                 number: str = None,
                 number_type: CallNumberType = None,
                 phonebook_entry: str = None,
                 ):
        """
        This class represents a call object.

        :param call_id: The ID of the call, usually a continuous integer.
        :param oriented: The orientation of the call, True for outgoing, False for incoming.
        :param state: The state of the call.
        :param service_mode: The mode of bearer/tele service of this call.
        :param multiparty: Whether the call is multiparty call.
        :param number: The number of the call, as the number_type specifies.
        :param number_type: The type of the number.
        :param phonebook_entry: The phonebook entry of the number.
        """
        self.call_id = call_id
        self.oriented = oriented
        self.state = state
        self.service_mode = service_mode
        self.multiparty = multiparty
        self.number = number
        self.number_type = number_type
        self.phonebook_entry = phonebook_entry

    def __eq__(self, other):
        if not isinstance(other, Call):
            return NotImplemented

        if self.call_id != other.call_id:
            return False
        if self.oriented != other.oriented:
            return False
        if self.service_mode != other.service_mode:
            return False
        if self.multiparty != other.multiparty:
            return False
        if self.number != other.number:
            return False
        if self.number_type != other.number_type:
            return False
        if self.phonebook_entry != other.phonebook_entry:
            return False

        return True

    @classmethod
    def from_list_call(cls, response: str):
        """
        This method creates a Call object from a list call response.

        :param response: One line of the list call response.
        :return: A Call object.
        """

        pattern = re.compile(r'\+CLCC: (\d+),(\d+),(\d+),(\d+),(\d+)((,"[^"]+",\d+)(,".*")?)?')

        match = pattern.match(response)

        if match:
            groups = match.groups()

            call_id = int(groups[0])
            oriented = bool(int(groups[1]))
            state = CallState(int(groups[2]))
            service_mode = BearerServiceMode(int(groups[3]))
            multiparty = bool(int(groups[4]))

            if groups[5]:
                combined_str = groups[6].strip(',')
                number = combined_str.split(',')[0].strip('"')
                number_type = CallNumberType(int(combined_str.split(',')[1]))
            else:
                number = None
                number_type = None

            if groups[7]:
                phonebook_entry = groups[7].strip(',"')
            else:
                phonebook_entry = None

            return cls(
                call_id=call_id,
                oriented=oriented,
                state=state,
                service_mode=service_mode,
                multiparty=multiparty,
                number=number,
                number_type=number_type,
                phonebook_entry=phonebook_entry,
            )
        else:
            raise ValueError('Invalid response')
