from pathlib import Path
from datetime import datetime

THIS_FILE = Path(__file__)
LOG_FILE = THIS_FILE.parent.parent / 'log.txt'


def format_date_time(date_time: datetime):
    return date_time.strftime(r"%Y-%m-%d %H:%M:%S")


def log(message, app='thread_switcher'):
    message = f"{format_date_time(datetime.now())} {app} - {message}"
    print(message)
    with open(LOG_FILE, 'a') as f:
        f.write(f'{message}\r\n')
