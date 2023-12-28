from enum import Enum 
import random

class RESET_MODE(Enum):
    EARLY = 'earliest'
    LATE = 'latest'

ACTIVE_RESET_MODE = RESET_MODE.LATE

DONE = 'd8n-done'
LINES = 'd8n-lines'
SYMBOLS = 'd8n-symbols'
TEXT = 'd8n-text'
CLEANUP= 'd8n-cleanup'
ORIGINAL='d8n-ORIGINAL'

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


def get_next_from_status(status: ItemStatus):
    is_failed = Status.Failed in Status(status.finished_tasks)

    if is_failed:
        return DONE

    is_symbol = Status.Symbol_Detection in Status(status.finished_tasks)
    is_line = Status.Line_Detection in Status(status.finished_tasks)
    is_text = Status.Text_Extraction in Status(status.finished_tasks)

    is_clean = Status.Cleanup in Status(status.finished_tasks)

    arr = [(is_symbol, SYMBOLS),
           (is_line, LINES),
           (is_text, TEXT)]
    random.shuffle(arr)

    all_ok = True
    for node in arr:
        if not node[0]:
            all_ok = False

    if all_ok:
        if is_clean:
            return DONE
        else:
            return CLEANUP
    else:
        for node in arr:
            if not node[0]:
                return node[1]
