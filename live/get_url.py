import requests
import re
import os
from live.log import log


def get_room_info(user_id):
    url = f"https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={user_id}"
    user_info = requests.get(url)

    code = user_info.status_code
    if not code == 200:
        log.error(f"request user info failed, status {code}")
        return None

    if not user_info.json()["data"]["roomStatus"]:
        log.error("space info error, skip")
        return None

    return user_info.json()


def get_room_id(room_info):
    room_url = room_info["data"]["url"]
    room_id = re.findall(r"\d+", room_url)[0]
    log.info(f"room_id is {room_id}")

    return room_id


def get_room_title(room_info):
    title = room_info["data"]["title"]
    log.info(f"room title is {title}")
    return title


def get_live_status(room_id):
    url = f"https://api.live.bilibili.com/room/v1/Room/room_init?id={room_id}"
    res = requests.get(url)

    code = res.status_code
    if not code == 200:
        log.error(f"request live status failed, status {code}")
        return None

    # status == 1 -> live on; status ==0 -> live off
    live_status = res.json()["data"]["live_status"]
    return live_status


def get_stream_url(room_id):
    quality = 10000  # 原画画质
    stream_info_url = (
        "https://api.live.bilibili.com/xlive/web-room/v1/index/"
        f"getRoomPlayInfo?room_id={room_id}&play_url=1&mask=1&"
        f"qn={quality}&platform=web"
    )
    res = requests.get(stream_info_url)

    code = res.status_code
    if not code == 200:
        log.error(f"parse stream url failed, status {code}")
        return None

    stream_info = res.json()
    stream_url = stream_info["data"]["play_url"]["durl"][0]["url"]

    return stream_url
