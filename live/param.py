from pathlib import Path
from yarl import URL


class Fpath:
    # config file path
    user_home = Path.home()
    config_file = user_home.joinpath('.config/livelist.toml')
    save_dir = user_home.joinpath('Videos/bilibili')

    # logs
    errlog = save_dir.joinpath('err.log')
    info = save_dir.joinpath('info.log')

class Api:
    # bilibili api
    _base = URL('https://api.live.bilibili.com/')
    _base_space = URL('https://api.bilibili.com/')
    _user = 'x/space/acc/info'
    _room_from_uid = 'room/v1/Room/getRoomInfoOld'
    _room = 'room/v1/Room/get_info'
    _status = 'room/v1/Room/room_init'
    _stream = 'xlive/web-room/v1/index/getRoomPlayInfo'

    def __init__(self):
        self.user_info = self.set_url(self._base_space, self._user, 'mid')
        self.room_from_uid = self.set_url(self._base, self._room_from_uid, 'mid')
        self.room_info = self.set_url(self._base, self._room, 'id')
        self.live_status = self.set_url(self._base, self._status, 'id')

        self.stream_opt = {
            'room_id': '',
            'play_url': 1,
            'mask': 1,
            'qn': 10000,
            'platform': 'web'
        }
        self.stream_api = self.set_url(self._base, self._stream,
                                       **self.stream_opt)

    def set_url(self, base, path, *args, **kwds):
        url = base.with_path(path)
        for q in args:
            url = url.update_query({q: ''})

        for k, v in kwds.items():
            url = url.update_query({k: v})

        return url

    def set_mid(self, room_id):
        self.room_info = self.room_info.update_query({'id': room_id})
        self.live_status = self.live_status.update_query({'id': room_id})
        self.stream_api = self.stream_api.update_query({'room_id': room_id})

    def set_uid(self, user_id):
        self.user_info = self.user_info.update_query({'mid': user_id})
        self.room_from_uid = self.room_from_uid.update_query({'mid': user_id})

    def set_qn(self, qn):
        self.stream_api = self.stream_api.update_query({'qn': qn})


