from threading import Thread

from live.task import Watcher
from live.args import cmd


def main():
    config_file = cmd()["config"]
    cctv = Watcher(config_file)

    c = Thread(target=cctv.watch_config)
    s = Thread(target=cctv.watch_live_status)
    l = Thread(target=cctv.watch_recorders)
    t = Thread(target=cctv.tasks)
    for t in [c, s, l, t]:
        t.start()
