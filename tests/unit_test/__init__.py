from unittest.mock import AsyncMock, MagicMock, patch


class MockSerial:
    """
    This is a simple mock of the serial.Serial class. It is used
    to mock the serial.Serial class to avoid making actual serial
    connections during testing.
    """

    def __init__(self, *args, **kwargs):
        self.port = args[0]
        self.baudrate = args[1]

        self._input_buffer = b''
        self._output_buffer = b''

        self._responses = []
        self._should_raise = kwargs.get('should_raise', False)
        self._default_response = kwargs.get('default_response', b'')

    def add_response(self, response: dict[str, bytes]):
        """
        This method adds a response with a matching input to the mock.
        """

        self._responses.append(response)

    def reset_input_buffer(self):
        self._input_buffer = b''

    def reset_output_buffer(self):
        self._output_buffer = b''

    def in_waiting(self):
        return len(self._input_buffer)

    def out_waiting(self):
        return len(self._output_buffer)

    def _respond(self, input_data: bytes) -> bytes:
        """
        This method finds a matching response for the input data and
        returns the response.

        If no matching response is found, it returns the default response.
        or raises an exception.
        """

        for response in self._responses:
            if response['input'] == input_data:
                return response['output']

        if self._should_raise:
            raise Exception('No matching response found')

        return self._default_response

    def write(self, data):
        """
        This method is used to simulate writing data to the serial port.
        """

        self._output_buffer += data

        response = self._respond(data)
        self._input_buffer += response

    def read(self, size=1):
        """
        This method is used to simulate reading data from the serial port.
        """

        data = self._input_buffer[:size]
        self._input_buffer = self._input_buffer[size:]

        return data
