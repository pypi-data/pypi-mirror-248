from .config import OpenMLHubConf
from .client import OpenMLHubClient
from .logger import Logger


def model_logger(conf: OpenMLHubConf):
    """ Create a specific model logger to share trainning and model infomration
        with OpenMLHub
    """
    client = OpenMLHubClient(conf)
    return Logger(client)