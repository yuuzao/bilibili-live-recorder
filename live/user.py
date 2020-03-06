import requests
import re
import os
from yarl import URL

from live.param import Api, Header
from live.log import log


class User:
    def __init__(self, user_info, qn=None):
        self.qn = qn
        self.live_time = None
        self.live_frequency = None

        self.user_name = None
        self.uid = None
        self.mid = None
        self.room_title = None
        self.live_status = 0
        self.stream_url = None

        self.api = Api()

        self.parse_user_info(user_info)

    def get_user_name(self):
        res = self._req(self.api.user_info)
        if not res['err']:
            user = res['res']
            self.user_name = user.json()['data']['name']
            log.info(f'get user name: {self.user_name}')
        else:
            log.info(f"get user name failed, status {res['code']}")

    def get_room_from_uid(self):
        res = self._req(self.api.room_from_uid)
        if not res['err']:
            room = res['res']
            room_url = URL(room['data']['url'])

            self.mid = room_url.parts[-1]
            self.room_title = room['data']['title']
            self.live_status = room['data']['liveStatus']
            log.info(f'get room title: {self.room_title}, live status {self.live_status}')
        
        else:
            log.info(f"get room info failed, status {res['code']}")

    def get_room_from_mid(self):
        res = self._req(self.api.room_info)
        if not res['err']:
            room = res['res']
            self.uid = room['data']['uid']
            self.room_title = room['data']['title']
            self.live_status = room['data']['live_status']
            log.info(f'get room title: {self.room_title}, live status {self.live_status}')
            self.get_user_name()

        else:
            log.info(f"get room info failed, status {res['code']}")

    def get_live_status(self):
        res = self._req(self.api.live_staus)

        if not res['err']:
            # staus == 1 -> live on; staus == 0 -> live off
            self.live_status = res['res']['data']['live_status']
            log.info(f"room {self.room_title} in status {self.live_status}")
        
        else:
            log.info(f'get live status failed, status {res["code"]}')
    
    def get_stream_url(self):
        res = self._req(self.api.stream_url)
        if not res['err']:
            self.stream_url = res['res']['data']['play_url']['durl'][0]
            log.info(f"get stream url {self.stream_url}")
        
        else:
            log.info(f"fetch live stream failed, status {res['code']}")

    def parse_user_info(self, user_info):
        self.live_frequency = user_info['frequency']
        self.live_time = user_info['live_time']

        url  = user_info['url']
        id = self._parse_id(url)
        if 'live.bilibili.com' in url:
            self.mid = id
            self.api.set_mid(id)
        if 'space.bilibili.com' in url:
            self.uid = id
            self.api.set_uid(id)
            self.get_user_name()
            self.get_room_from_uid()

    @staticmethod
    def _req(url):
        headers = Header(url)
        res = requests.get(url, headers=headers)

        code = res.status_code
        if code < 400:
            return {'err': True, "code": code}

        return {'err': False, 'res': res.json()}

    @staticmethod
    def _parse_id(url):
        """
        return the id of the given space url or room url.
        """
        return re.findall(r'/\d+', url)[0][1:]
