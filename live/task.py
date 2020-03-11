# monitor config file
# monitor live status
import asyncio

from live.log import log
from live.user import User
from live.utils import naming
from live.recorder import Rec
from live.livelist import Files, Livelist

class Lives:
    def __init__(self, config_file=None, save_dir=None):
        self.lives = Livelist(config_file, save_dir)
        self.stream_suffix = 'flv'
    
    async def watch_config(self):
        while True:
            if self.lives.reconfigured:
                self.lives.parse_user_config()
                self.lives.assmble_users()
            else:
                log.info('Configuration remains the same, will be checked again after 60 seconds')
            # set this at the bottom to ensure the first loop will parse user info
            self.lives.config_changed()
            await asyncio.sleep(60)

    async def watch_lives_staus(self):
        while True:
            livings = 0
            for user in self.lives.users:
                if user.live_status == 1:
                    livings += 1
                    continue
                await user.get_live_status()
            log.info(f"{livings} lives is online")
            await asyncio.sleep(10)
    
    async def record(self):
        while True:
            for user in self.lives.users:
                if user.live_status == 1 and user.is_recording is False:
                    log.info(f"Detect live [{user.room_title}] on...")
                    user.is_recording = True

                    # this cannot be awaited...
                    asyncio.create_task(self._rec(user, user.room_title, self.lives.sdir))

            # there must be a sleep to block this while loop
            await asyncio.sleep(10)

    @staticmethod
    async def _rec(user, name, sdir):
        user.get_stream_url()
        r = Rec(user.stream_url, name, sdir)

        await asyncio.gather(r.record(), r.rec_stat())

        user.is_recording = False
        user.live_status = 0
