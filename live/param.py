from pathlib import Path
from yarl import URL


class Config:
    # path
    user_home = Path.home()
    config_file = user_home.joinpath('.config/livelist.toml')
    save_dir = user_home.joinpath('Videos/bilibili')


class Api:
    # bilibili api
    _base = URL('https://api.live.bilibili.com/')
    _room = 'room/v1/Room/getRoomInfoOld'
    _status = 'room/v1/Room/room_init'
    _stream = 'xlive/web-room/v1/index/getRoomPlayInfo'

    def __init__(self):
        self.room_url = self.set_url(self._base, self._room, 'mid')
        self.live_staus = self.set_url(self._base, self._status, 'id')

        self.stream_opt = {
            'room_id': '',
            'play_url': 1,
            'mask': 1,
            'qn': '',
            'platform': 'web'
        }
        self.stream_url = self.set_url(self._base, self._stream,
                                       **self.stream_opt)

    def set_url(self, base, path, *args, **kwds):
        url = base.with_path(path)
        for q in args:
            url = url.update_query({q: ''})

        for k, v in kwds.items():
            url = url.update_query({k: v})

        return url

    def set_mid(self, room_id):
        self.room_url = self.room_url.update_query({'mid': room_id})
        self.live_staus = self.live_staus.update_query({'id': room_id})
        self.stream_url = self.stream_url.update_query({'room_id': room_id})

    def set_qn(self, qn):
        self.stream_url = self.stream_url.update_query({'qn': qn})
