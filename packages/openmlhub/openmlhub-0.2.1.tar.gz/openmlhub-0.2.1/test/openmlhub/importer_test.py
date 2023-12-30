import tempfile
import json

import pytest
from unittest.mock import Mock

from openmlhub.importer import Importer
from openmlhub.model import ModelMetadata
from openmlhub.metric import TrainningEpocMetric


@pytest.fixture
def mock_client(mocker):
    mock = Mock()
    return mock

def test_importer_can_read_metadata(mock_client):
    importer = Importer(mock_client)
    
    metric = TrainningEpocMetric(2,"loss", [0.0, 0.1])
    metadata = ModelMetadata("id123","vers123", [ metric ])

    with tempfile.TemporaryDirectory() as tempdirname:
        with open(tempdirname + "/metadata.json", 'w', encoding='UTF-8') as fd:
            json.dump(metadata.to_dict(), fd)     

        importer.import_logs(tempdirname)    
    assert mock_client.log.call_args.args[0].model_id == 'id123'
    assert mock_client.log.call_args.args[0].version == 'vers123'
    assert mock_client.log.call_args.args[0].metrics[0].metric_name == 'loss'
