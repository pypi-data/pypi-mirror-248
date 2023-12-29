from enum import StrEnum

class Metric:
    """ Basic metric representing a mesurement.
    """
    def to_dict(self):
        pass


class TrainningMetric(StrEnum):
    """ List of known trainning metrics
    """
    LOSS = "loss"
    ACC = "acc"
    F1 = "f1"
    AUC = "auc"


class TrainningEpocMetric(Metric):
    def __init__(self, epocs: int, metric_name: TrainningMetric, measurement: list[float]) -> None:
        super().__init__()
        self.epocs = epocs
        self.metric_name = metric_name
        self.measurement = measurement
        
    def to_dict(self):
        return {
            'type': 'TrainningEpocMetric',
            'epocs': self.epocs,
            'name': self.metric_name,
            'measurement': self.measurement
        }