import time
from src.log import log

def watch(fn, switch_every_n_seconds):
    words = ['FATAL ERROR']

    c = 0
    fp = open(fn, 'r')
    fp.seek(0, 2)
    while c < switch_every_n_seconds:
        new_line = fp.readline()
        if new_line:
            log(new_line.rstrip(), 'prime95')
            if 'FATAL ERROR' in new_line:
                yield new_line
    
        time.sleep(1)
        c += 1

def monitor_for_errors(fn, switch_every_n_seconds):
    for line in watch(fn, switch_every_n_seconds):
        msg = f"Found fatal error: {line}"
        log(msg)
        raise Exception(msg)