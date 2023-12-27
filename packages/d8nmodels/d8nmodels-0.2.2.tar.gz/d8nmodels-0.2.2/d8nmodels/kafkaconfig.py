from enum import Enum 

class RESET_MODE(Enum):
    EARLY = 'earliest'
    LATE = 'latest'

ACTIVE_RESET_MODE = RESET_MODE.LATE

DONE = 'd8n-done'
LINES = 'd8n-lines'
SYMBOLS = 'd8n-symbols'
TEXT = 'd8n-text'
CLEANUP= 'd8n-cleanup'

