import asyncio
from yarl import URL

from live.param import Api
from live.utils import req, sreq
from live.log import log


class User:
    def __init__(self, user_info, manual=False):
        self.qn = None
        self.live_time = None
        self.live_frequency = None

        self.user_name = None
        self.uid = None
        self.mid = None
        self.room_title = None
        self.live_status = 0
        self.stream_url = None

        # is case of user is 404, will be updated later
        # self.is_akarin = True

        self.is_recording = False

        self.api = Api()
        
        if not manual:
            log.info("=========")
            self._update_user(user_info)

    def get_user_name(self):
        log.info(f"Fetching user name with uid [{self.uid}], url is ]{self.api.user_info}]")
        res = sreq(self.api.user_info)
        if not res['err']:
            self.is_akarin = False
            user = res['res']
            self.user_name = user['data']['name']
            log.info(f'get user name: [{self.user_name}]')
        else:
            self.is_akarin = True
            log.info(f"get user name failed, url is [{self.api.user_info}], status [{res['code']}]")

    def get_room_from_uid(self):
        log.info(f"Updating room info with uid [{self.uid}], url is [{self.api.room_from_uid}]")
        res = sreq(self.api.room_from_uid)
        if not res['err']:
            room = res['res']
            room_url = URL(room['data']['url'])

            self.mid = room_url.parts[-1]
            self.room_title = room['data']['title']
            self.live_status = room['data']['liveStatus']

            self.api.set_mid(self.mid)
            log.info(f'get room title: [{self.room_title}], live status [{self.live_status}]')
        
        else:
            log.info(f"get room info failed, url is: [{self.api.room_from_uid}], [status {res['code']}]")

    def get_room_from_mid(self):
        log.info(f"Updating room info from mid [{self.mid}], url is [{self.api.room_info}]")
        res = sreq(self.api.room_info)
        if not res['err']:
            room = res['res']
            self.uid = room['data']['uid']
            self.room_title = room['data']['title']
            self.live_status = room['data']['live_status']
            log.info(f'get room title: [{self.room_title}], live status [{self.live_status}]')

            self.api.set_uid(self.uid)
            self.get_user_name()

        else:
            log.info(f"get room info failed, url is [{self.api.room_info}], status [{res['code']}]")

    async def get_live_status(self):
        log.info(f"Updating live status for [{self.user_name}], url is [{self.api.live_status}]")
        res = await req(self.api.live_status)

        if not res['err']:
            # staus == 1 -> live on; staus == 0 -> live off
            self.live_status = res['res']['data']['live_status']
            log.info(f"room [{self.room_title}] in status [{self.live_status}]")
        
        else:
            log.info(f'get live status failed, room id is [{self.mid}] , status [{res["code"]}]')
    
    def get_stream_url(self):
        log.info(f"Fetching live stream url for [{self.room_title}]")
        res = sreq(self.api.stream_api)
        if not res['err']:
            self.stream_url = URL(res['res']['data']['play_url']['durl'][0]['url'])
            log.info(f"Stream url is [{self.stream_url}]")
        
        else:
            log.info(f"fetch live stream failed, status [{res['code']}]")

    def _update_user(self, user_info):
        self.live_frequency = user_info['frequency']
        self.live_time = user_info['live_time']
        self.qn = user_info['quality']

        if user_info['mid'] is not None:
            self.mid = user_info['mid']
            self.api.set_mid(self.mid)
            self.get_room_from_mid()
        else:
            self.uid = user_info['uid']
            self.api.set_uid(self.uid)
            
            self.get_user_name()
            self.get_room_from_uid()
