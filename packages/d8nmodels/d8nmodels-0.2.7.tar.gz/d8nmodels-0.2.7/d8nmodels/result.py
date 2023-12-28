import datetime
from typing import Any

class ExtractionResult(dict):
    timestamp: float = 0
    request_handle: str = ''
    userId: str = ''
    data: Any
    type : str
    time : datetime.datetime 