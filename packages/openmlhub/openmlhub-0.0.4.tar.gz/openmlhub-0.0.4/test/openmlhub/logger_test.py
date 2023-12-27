import pytest
from unittest.mock import Mock

from openmlhub import Logger
from openmlhub import OpenMLHubClient

@pytest.fixture
def mock_client(mocker):
    mock = Mock()
    return mock

def test_logger_create_metadata_with_id_version(mock_client):
    Logger(mock_client, "model-id-123").log()
    assert mock_client.log.called_once()
