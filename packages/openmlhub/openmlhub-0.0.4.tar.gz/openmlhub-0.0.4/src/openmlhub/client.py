import requests

from .config import OpenMLHubConf
from .model import ModelMetadata

class OpenMLHubClientError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class OpenMLHubClient:
    """ This client implements the communication with OpenMLHub
    """
    def __init__(self, conf: OpenMLHubConf) -> None:
        self.conf = conf

            
    def log(self, metadata: ModelMetadata) -> None:
        """ Implement data logging
        """
        resp = requests.post('https://openmlhub.com/log_model',
            headers= {
                'uid': self.conf.uid,
                'api_key': self.conf.api_key
            },
            json=metadata.to_dict())

        if resp.status_code != 201:
            raise OpenMLHubClientError(f"log model, invalid response: {resp.status_code}")