import pytest
import numpy as np

from unittest.mock import Mock

from openmlhub import Logger

@pytest.fixture
def mock_client(mocker):
    mock = Mock()
    return mock

def test_logger_create_metadata_with_id_version(mock_client):
    Logger(mock_client, "model-id-123").log()
    assert mock_client.log.called_once()

def test_logger_create_metadata_with_mesurement(mock_client):
    (Logger(mock_client, "model-id-123")
        .with_f1_epoc(np.array([0.0, 0.1]))
        .with_loss_epoc(np.array([0.0, 0.2]))
        .log())

    assert mock_client.log.called_once()