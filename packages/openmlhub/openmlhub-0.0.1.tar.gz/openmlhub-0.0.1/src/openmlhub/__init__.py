class OpenMLHubConf:
    def __init__(self, uid: str, api_key: str, model_id: str) -> None:
        self.uid = uid
        self.api_key = uid
        self.model_id = model_id


def model_logger(conf):
    