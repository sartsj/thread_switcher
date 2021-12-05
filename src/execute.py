from subprocess import run
from datetime import datetime as dt
from typing import Iterable

from src.core import Core, get_cores, get_index_of_core_in
from src.log import format_date_time, log
from src.timing import wait_and_sync
from src.monitor import monitor_for_errors


def execute(cfg: dict):

    cores = get_cores(cfg["hyper_threading"], cfg["core_num"])

    try:
        for core in get_infinite_core_iterator(cores, cfg["starting_core"]):
            log_starting_core(core)
            set_active_core_for(core, cfg["process_to_switch"])
            monitor_for_errors(cfg["p95_results_file"], cfg["switch_every_n_seconds"])

    except KeyboardInterrupt as e:
        print("Stopped")
        raise(e)


def log_starting_core(core: Core):
    log(f"Switching to {core}")


def set_active_core_for(core: Core, process_name: str) -> None:
    run('Powershell "ForEach($PROCESS in'
        + f' GET-PROCESS {process_name})'
        + ' { $PROCESS.ProcessorAffinity=' + core.affinity_mask
        + '}"')


def get_infinite_core_iterator(cores: list[Core],
                               starting_core_friendly_number: int) \
        -> Iterable[Core]:
    starting_index = get_index_of_core_in(starting_core_friendly_number, cores)
    return get_infinite_iterator(cores, starting_index)


def get_infinite_iterator(collection: list,
                          starting_index: int) \
        -> Iterable:
    length = len(collection)
    i = starting_index
    while True:
        if i >= length:
            i = 0
        yield collection[i]
        i += 1


if __name__ == '__main__':
    main()
