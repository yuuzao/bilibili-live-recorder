import re
import time
import shutil
import subprocess
import requests
from functools import wraps
from live.log import log

import live.get_url as Live


def read_config(conf):
    if not conf.exists():
        log.error("config file does not exitsts")
        return None

    raw = conf.read_text()
    space_ids = re.findall(r"\d+", raw)

    return space_ids


def parse_user(user_id):
    user_info = Live.get_room_info(user_id)
    if user_info is None:
        return None

    title = Live.get_room_title(user_info)
    room_id = Live.get_room_id(user_info)

    return {"user_id": user_id, "room_title": title, "room_id": room_id}


def download(url, file):
    c = 2
    while c < 4:
        log.info(f"recording to {file}")
        with requests.get(url, stream=True) as r:
            if r.status_code != 200:
                log.info(f"status {r.status_code}, retrying for {c}th times")
                c += 1
                continue
            with open(file, "wb") as f:
                shutil.copyfileobj(r.raw, f)
                log.info(f"{file} recorded")
                log.info(f"exit with status {r.status_code}")
                return

    log.info("Max retries exceeded with url, please check you network")
    return
