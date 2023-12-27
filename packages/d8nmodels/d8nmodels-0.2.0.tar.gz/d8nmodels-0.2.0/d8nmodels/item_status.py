import datetime
from uuid import uuid4
from flags import Flags

class PredictionOutput(object):

    def to_output(self):
        return {
            "x1": self.x1,
            "x2": self.x2,
            "y1": self.y1,
            "y2": self.y2,
            "text": self.text,
            "conf": self.confidence,
            "class": self._class,
            "type": self.type
        }

    def __init__(self, x1: float, y1: float, x2: float, y2: float, _conf: float,
                 _class: str, currType: str, segment: list[float]):
        self.prediction_id = str(uuid4())
        self._class = _class
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.confidence = _conf
        self.type = currType
        self.segment = segment
        self.text = []


class Status(Flags):
    Pending = 1
    Started = 2
    Symbol_Detection = 4
    Line_Detection = 8
    Text_Extraction = 16
    Rejected = 32
    Failed = 64
    Completed = 128,
    Cleanup= 256


class ItemStatus():

    def __init__(self, dictionary:dict):
         for k, v in dictionary.items():
             setattr(self, k, v)

    userId: str
    device_id: str
    request_id: str
    request_handle: str
    current_task: int = int(Status.Started)
    finished_tasks: int = int(Status.Started)
    working_path_symbols: str
    working_path_lines: str
    working_path_text: str
    path : str
    last_update : datetime
    path_url:str
    is_experimental:bool