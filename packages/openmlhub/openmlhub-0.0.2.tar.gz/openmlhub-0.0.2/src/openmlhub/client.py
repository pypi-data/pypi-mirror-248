import requests

from .config import OpenMLHubConf

class OpenMLHubClientError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class OpenMLHubClient:
    """ This client implements the communication with OpenMLHub
    """
    def __init__(self, conf: OpenMLHubConf) -> None:
        self.conf = conf

            
    def log(self):
        """ Implement data loging
        """
        resp = requests.post('https://openmlhub.com/model_log',
            headers= {
                'uid': self.conf.uid,
                'api_key': self.conf.api_key
            },
            json={})

        if resp.status_code != 201:
            raise OpenMLHubClientError("log model, invalid response: {resp.status_code}")