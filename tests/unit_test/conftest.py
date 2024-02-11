import pytest
from unittest.mock import patch


@pytest.fixture(scope="class", autouse=True)
def mock_device(request):
    if 'no_autouse' in request.keywords:
        yield False

    try:
        with patch(f'{request.param}.device') as mock_device:
            yield mock_device
    except AttributeError:
        yield False
