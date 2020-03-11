import os
import re
import asyncio
import toml
from pathlib import Path

from live.param import Fpath
from live.user import User
from live.log import log


class Files:
    def __init__(self, config_file=None, save_dir=None):
        self.fconfig = [Path(config_file) if config_file is not None else Fpath.config_file][0]
        self.sdir = self.parse_save_dir(save_dir)
        self.mtime = os.stat(self.fconfig).st_mtime

        # set True to ensure the first loop won't be skipped
        self.reconfigured = True
    
    def parse_save_dir(self, v):
        if v is not None:
            s = v
        else:
            t = toml.load(self.fconfig)
            if 'save_dir' in t:
                s = t['save_dir']
            else:
                s = Fpath.save_dir
        if not s.exists():
            log.info(f"Creating saving directory at {s}")
            s.mkdir(parents=True)

        return Path(s)

    def config_changed(self):
        st = os.stat(self.fconfig).st_mtime
        if self.mtime == st:
            self.reconfigured = False
        else:
            self.mtime = st
            self.reconfigured = True



class Livelist(Files):
    def __init__(self, config_file=None, save_dir=None):
        super().__init__(config_file=config_file, save_dir=save_dir)
        self.live_list = []
        self.users = []

    def parse_user_config(self):
        log.info(f'Start to read configurations from {self.fconfig}')
        cf = toml.load(self.fconfig)
        for u in cf['users']:
            log.info(f"Loading user: {u['url']}")
            self.live_list.append(u)
        log.info(f"Loaded {len(self.live_list)} users in total")

    def assmble_users(self, m=False):
        for c in self.live_list:
            _c = self._user_info(c)
            u = User(_c, m)
            if u.is_akarin is False:
                self.users.append(u)
            else:
                log.info(f"Akarin user: {c['url']}, omitted...")
    
    def _user_info(self, config):
        for k in ['uid', 'mid', 'live_time']:
            config.setdefault(k)
        
        config.setdefault('frequency', 3600)
        config.setdefault('quality', 10000)
        
        link = config['url']
        id = self._parse_id(link)
        if 'live.bilibili.com' in link:
            config['mid'] = id
        else:
            config['uid'] = id
        
        return config
            
    @staticmethod
    def _parse_id(url):
        """
        return the id of the given space url or room url.
        """
        return re.findall(r'/\d+', url)[0][1:]