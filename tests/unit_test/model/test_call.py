from py_sim7600.model.enums import CallState, CallNumberType, BearerServiceMode
from py_sim7600.model.call import Call


class TestCall:
    def test_init(self):
        call = Call(
            call_id=1,
            oriented=True,
            state=CallState.ACTIVE,
            service_mode=BearerServiceMode.DATA,
            multiparty=True,
            number='1234567890',
            number_type=CallNumberType.INTERNATIONAL,
            phonebook_entry='test',
        )

        assert call.call_id == 1
        assert call.oriented
        assert call.state == CallState.ACTIVE
        assert call.service_mode == BearerServiceMode.DATA
        assert call.multiparty
        assert call.number == '1234567890'
        assert call.number_type == CallNumberType.INTERNATIONAL
        assert call.phonebook_entry == 'test'

    def test_from_list_call(self):
        response_1 = '+CLCC: 1,0,0,0,0,"10011",129,"sm"'
        response_2 = '+CLCC: 1,1,4,0,0,"02152063113",128,"gongsi"'

        call_1 = Call.from_list_call(response_1)
        call_2 = Call.from_list_call(response_2)

        assert call_1.call_id == 1
        assert not call_1.oriented
        assert call_1.state == CallState.ACTIVE
        assert call_1.service_mode == BearerServiceMode.VOICE
        assert not call_1.multiparty
        assert call_1.number == '10011'
        assert call_1.number_type == CallNumberType.OTHER
        assert call_1.phonebook_entry == 'sm'

        assert call_2.call_id == 1
        assert call_2.oriented
        assert call_2.state == CallState.INCOMING
        assert call_2.service_mode == BearerServiceMode.VOICE
        assert not call_2.multiparty
        assert call_2.number == '02152063113'
        assert call_2.number_type == CallNumberType.RESTRICTED
        assert call_2.phonebook_entry == 'gongsi'

    def test_from_list_call_short_response(self):
        response_1 = '+CLCC: 1,0,0,0,0,"10011",129'
        response_2 = '+CLCC: 1,1,4,0,0'

        call_1 = Call.from_list_call(response_1)
        call_2 = Call.from_list_call(response_2)

        assert call_1.call_id == 1
        assert not call_1.oriented
        assert call_1.state == CallState.ACTIVE
        assert call_1.service_mode == BearerServiceMode.VOICE
        assert not call_1.multiparty
        assert call_1.number == '10011'
        assert call_1.number_type == CallNumberType.OTHER
        assert call_1.phonebook_entry is None

        assert call_2.call_id == 1
        assert call_2.oriented
        assert call_2.state == CallState.INCOMING
        assert call_2.service_mode == BearerServiceMode.VOICE
        assert not call_2.multiparty
        assert call_2.number is None
        assert call_2.number_type is None
        assert call_2.phonebook_entry is None
