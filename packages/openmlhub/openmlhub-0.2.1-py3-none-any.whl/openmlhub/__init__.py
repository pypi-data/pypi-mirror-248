from .config import OpenMLHubConf
from .client import OpenMLHubClient
from .logger import Logger
from .importer import Importer # xD


def model_logger(conf: OpenMLHubConf, model_id: str, version: str = "draft"):
    """ Create a specific model logger to share trainning and model infomration
        with OpenMLHub
    """
    client = OpenMLHubClient(conf)
    return Logger(client, model_id, version)


def import_logs(conf: OpenMLHubConf, dir: str):
    client = OpenMLHubClient(conf)
    importer = Importer(client)
    importer.import_logs(dir)
    
 