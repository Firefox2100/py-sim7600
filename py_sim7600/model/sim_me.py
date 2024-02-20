from .enums import SIMMECommandType


class SIMMECommand:
    """
    Base class for SIM ME commands.
    """
    def __init__(self, command_type: SIMMECommandType, use_gsm_format: bool = True):
        """
        Base class for SIM ME commands.

        :param command_type: The type of the command.
        :param use_gsm_format: Whether to use GSM 11.11 format for the APDU.
        """
        self.command_type = command_type
        self.use_gsm_format = use_gsm_format

    @property
    def apdu(self) -> str:
        """
        The APDU format of the command, in ISO-7816 format.
        """

        if self.use_gsm_format:
            return self.apdu_gsm
        else:
            return self.apdu_iso

    @property
    def apdu_gsm(self) -> str:
        """
        The APDU format of the command, in GSM 11.11 format.
        """
        raise NotImplementedError

    @property
    def apdu_iso(self) -> str:
        """
        The APDU format of the command, in ISO-7816 format.
        """
        raise NotImplementedError


class SIMMECommandSelect(SIMMECommand):
    """
    A SELECT command for SIM ME.
    """
    def __init__(self, file_id: str):
        """
        A SELECT command for SIM ME.

        :param file_id: The file ID to select. It must be a 2-byte hex string.
        """

        super().__init__(SIMMECommandType.SELECT)

        # Ensure the file ID is 2 bytes hex string
        try:
            assert len(file_id) == 4
            assert all(c in "0123456789ABCDEF" for c in file_id)
        except AssertionError:
            raise ValueError("File ID must be a 2-byte hex string")

        self.file_id = file_id

    @property
    def apdu_gsm(self) -> str:
        return f"00A4000002{self.file_id}"


class SIMMEResponse:
    def __init__(self, command_type: SIMMECommandType, use_gsm_format: bool = True):
        self.command_type = command_type
        self.use_gsm_format = use_gsm_format

    @classmethod
    def parse(cls, command_type: SIMMECommandType, response: str) -> 'SIMMEResponse':
        raise NotImplementedError
