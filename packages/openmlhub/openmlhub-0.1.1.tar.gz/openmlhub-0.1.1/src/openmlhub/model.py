from .metric import Metric
class ModelMetadata:
    ''' Representation of sepecific model after trainning.
    '''
    def __init__(self ,model_id: str, version: str, metrics: list[Metric] = []):
        self.model_id = model_id
        self.version = version
        self.metrics = metrics
        
 
    def to_dict(self):
        '''Transform model  metadata to a dictionary'''
        return {
            'model_id': self.model_id,
            'version': self.version,
            'metrics': [metric.to_dict() for metric in self.metrics]
        }
