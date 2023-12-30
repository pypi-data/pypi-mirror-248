import json

from .client import OpenMLHubClient
from .model import ModelMetadata
from .metric import TrainningEpocMetric

class Importer:
    """ Enables importing model logs stored locally.
    """
    def __init__(self, client: OpenMLHubClient) -> None:
        self._client = client
        
    def import_logs(self, dir: str):
        metadata_path = dir + "/metadata.json"
        
        with open(metadata_path, 'r') as fd:
            metadata_json = json.load(fd)
            
            metrics = []
            # Handle individual type of metrics.
            if 'metrics' in metadata_json and metadata_json['metrics']:
                epoc_metrics = [TrainningEpocMetric(epocs=metric['epocs'],
                                                    metric_name=metric['name'],
                                                    measurement=metric['measurement']) 
                                for metric in metadata_json['metrics'] if metric['type'] == 'TrainningEpocMetric']
                metrics.extend(epoc_metrics)
                
            metadata = ModelMetadata(model_id=metadata_json['model_id'],
                                     version=metadata_json['version'],
                                     metrics=metrics)

            self._client.log(metadata)