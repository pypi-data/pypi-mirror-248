""" Logger implements logging funcionality for machine learnign models.
"""

from . import OpenMLHubConf

class Logger(object):
    def __init__(self, conf: OpenMLHubConf) -> None:
        self.conf = conf
