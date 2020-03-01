import time
import datetime
import os
import queue
from pathlib import Path
from functools import wraps
from threading import Thread, Lock

import live.get_url as Live
from live.log import log
import live.utils as utils


class Watcher:
    def __init__(self, config_file):
        super().__init__()
        self.config_file = Path(config_file)
        self.space_ids = set()
        # rooms: [{"user_id":xxx, "room_title":xxx, "room_id":xxx, "liveOn": bool, "mutable": bool}, ...]
        self.rooms = []

        # pre_loop is set to identify whether is the first loop. If true, a mutex is needed.
        self.pre_loop = True
        self.mutex = Lock()
        self.live_q = queue.Queue()  # queue of online lives
        self.recorders = []  # recorder threads

    def watch_config(self):
        file_stat = os.stat(self.config_file).st_mtime
        while True:
            if self.pre_loop:
                log.info("start to monitor config file.")
                self.mutex.acquire()

            st = os.stat(self.config_file).st_mtime
            if st == file_stat and not self.pre_loop:
                log.info("nothing new in config file")
                time.sleep(2)
                continue

            log.info("changes in config file have been detected.")
            file_stat = st

            s_ids = set(utils.read_config(self.config_file))

            new_ids = s_ids - self.space_ids
            discard_ids = self.space_ids - s_ids

            if len(new_ids) > 0:
                self.space_ids |= new_ids
                for id in new_ids:
                    new_room = utils.parse_user(id)
                    if new_room is None:
                        continue
                    new_room["liveOn"] = False
                    new_room["mutable"] = True
                    self.rooms.append(new_room)
                    log.info(
                        f"live room {new_room['room_title']}"
                        "is added into monitor process"
                    )
                    # be gentle
                    time.sleep(1)

            if len(discard_ids) > 0:
                self.space_ids -= discard_ids
                for id in discard_ids:
                    for r in self.rooms:
                        if r["user_id"] == id:
                            self.rooms.remove(r)
                            log.info(f"room {r['room_title']} is discarded")

            if len(new_ids) == 0 and len(discard_ids) == 0:
                log.info("No changes in space links")
                log.info("emmm, what have you done to config file?")

            if self.pre_loop:
                self.mutex.release()
                self.pre_loop = False
                log.info("pre loop finished, releasing lock...")
                log.info("====================================")
            time.sleep(60)

    def watch_live_status(self):
        while True:
            for room in self.rooms:
                if room["liveOn"] and not room["mutable"]:
                    log.info(f"live {room['room_title']} still be recording")
                    continue
                status = Live.get_live_status(room["room_id"])
                if status is None or status == 2:
                    log.info(f'{room["room_title"]} not online...')
                    continue
                if status == 1 and room["mutable"]:
                    room["liveOn"] = True
                    room["mutable"] = False
                    self.live_q.put(room)
                    log.info(
                        f"detect live {room['room_title']} on, preparing to record."
                    )
                time.sleep(1)
            time.sleep(2)

    def watch_recorders(self):
        while True:
            log.info("====================")
            if self.live_q.empty():
                log.info("no online lives at present, waiting")
                time.sleep(10)
                continue

            rec = Thread(target=self.recorder)
            self.recorders.append(rec)

            time.sleep(2)

    def tasks(self):
        while True:
            for rec in self.recorders:
                rec.start()
                self.recorders.remove(rec)

            time.sleep(2)

    def recorder(self):
        user_info = self.live_q.get()
        log.info(f"live task {user_info['room_title']} allocated, start recording")

        now = datetime.datetime.today().isoformat()[:19]
        file = user_info["room_title"] + "-" + now + ".flv"

        stream_url = Live.get_stream_url(user_info["room_id"])
        log.info(f"url is {stream_url}")

        utils.download(stream_url, file)

        r = self.rooms.index(user_info)
        self.rooms[r]["liveOn"] = False
        self.rooms[r]["mutable"] = True
