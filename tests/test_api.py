import pytest
import sys
from yarl import URL

from live.param import Api

room = URL('https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid=2233')
status = URL('https://api.live.bilibili.com/room/v1/Room/room_init?id=2233')
stream = URL("https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomPlayInfo?room_id=2233&play_url=1&mask=1&qn=10000&platform=web")


def test():
    api = Api()
    api.set_mid(2233)
    api.set_qn(10000)

    assert api.room_url == room
    assert api.live_staus == status
    assert api.stream_url == stream