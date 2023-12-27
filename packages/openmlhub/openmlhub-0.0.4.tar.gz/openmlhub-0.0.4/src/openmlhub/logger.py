""" Logger implements logging funcionality for machine learning models.
"""
from .client import OpenMLHubClient
from .model  import ModelMetadata

class Logger(object):
    """ This class collects infomration from the model and datasources, and 
        allow publish the data to OpenMLHub
    """
    def __init__(self, client: OpenMLHubClient, model_id: str, version: str = "draft") -> None:
        self._client = client
        self.model_id = model_id
        self.version = version
    
    def log(self):
        metadata = ModelMetadata(self.model_id, self.version)
        self._client.log(metadata)
