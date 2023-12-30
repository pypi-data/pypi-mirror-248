""" Logger implements logging funcionality for machine learning models.
"""
import numpy as np
import os 
import json

from .client import OpenMLHubClient
from .model  import ModelMetadata
from .metric import TrainningEpocMetric

class Logger(object):
    """ This class collects infomration from the model and datasources, and 
        allow publish the data to OpenMLHub
    """
    def __init__(self, client: OpenMLHubClient, model_id: str, version: str = "draft") -> None:
        self._client = client
        self.model_id = model_id
        self.version = version
        
        self.metrics = []

    def _with_metric_epoc(self, metric_name: str,  measurement: np.array):
        # TODO: Metric name use to be a StrEnum but not supported in 3.10, update onces enabled.
        self.metrics.append(
            TrainningEpocMetric(len(measurement), metric_name, measurement.tolist()))
        return self

    def with_loss_epoc(self, measurement: np.array):
        """ Add loss mesurement """
        return self._with_metric_epoc("loss", measurement)

    def with_f1_epoc(self, measurement: np.array):
        """ Add f1 mesurement """
        return self._with_metric_epoc("f1", measurement)

    def with_uac_epoc(self, measurement: np.array):
        """ Add loss mesurement """
        return self._with_metric_epoc("uac", measurement)

    def with_acc_epoc(self, measurement: np.array):
        """ Add accuracy mesurement """
        return self._with_metric_epoc("acc", measurement)

    
    def log(self):
        metadata = ModelMetadata(self.model_id, self.version, self.metrics)
        self._client.log(metadata)
    
    def log_to_local(self, dir: str = None):
        """For HPC systems without node access to internet, this allow to 
           create a temporal storage of repository artifact
           to be uploaded in a separate step.
        """
        metadata = ModelMetadata(self.model_id, self.version, self.metrics)
        
        # Store in the working directory.
        path = metadata.version
        if dir:
            path = f'{dir}/{metadata.version}'
        os.mkdir(path)
        
        with open(f'{path}/metadata.json', 'w', encoding="utf-8") as meta_fd:
            json.dump(metadata.to_dict(), meta_fd)
