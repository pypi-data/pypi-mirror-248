class Metric:
    """ Basic metric representing a mesurement.
    """
    def to_dict(self):
        pass


class TrainningEpocMetric(Metric):
    def __init__(self, epocs: int, metric_name: str, measurement: list[float]) -> None:
        super().__init__()
        self.epocs = epocs
        self.metric_name = metric_name
        self.measurement = measurement
    
    def __repr__(self) -> str:
        return f'TrainningEpocMetric({self.metric_name})'
        
    def to_dict(self):
        return {
            'type': 'TrainningEpocMetric',
            'epocs': self.epocs,
            'name': self.metric_name,
            'measurement': self.measurement
        }