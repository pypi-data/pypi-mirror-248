""" Logger implements logging funcionality for machine learning models.
"""

from .client import OpenMLHubClient

class Logger(object):
    """ This class collects infomration from the model and datasources, and 
        allow publish the data to OpenMLHub
    """
    def __init__(self, client: OpenMLHubClient, version: str = "draft") -> None:
        self._client = client
        self.version = version
        

    def log(self):
        self._client.log()
        

