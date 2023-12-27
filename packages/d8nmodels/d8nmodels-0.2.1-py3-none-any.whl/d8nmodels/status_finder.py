import random
from .item_status import ItemStatus, Status
from .kafkaconfig import LINES, SYMBOLS, TEXT, DONE, CLEANUP

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
