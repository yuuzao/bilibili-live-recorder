import os
import re
import toml

from live.param import Fpath
from live.user import User
from live.log import log


class Files:
    def __init__(self, config_file=None):
        self.fconfig = [config_file if config_file is not None else Fpath.config_file]
        self.mtime = os.stat(self.fconfig).st_mtime
    
    def parse_config(self):
        # In case of new entries in config file...
        log.info('Analysing config file')
    
    def is_changed(self):
        st = os.stat(self.fconfig).st_time
        if self.mtime == st:
            return False
        self.mtime = st
        return True


class Livelist(Files):
    def __init__(self, config_file=None):
        super().__init__(config_file=config_file)
        self.live_list = []
        self.users = []

    def parse_user_config(self):
        log.info(f'Start to read configurations from {self.fconfig}')
        cf = toml.load(self.fconfig)
        for u in cf['users']:
            log.info(f"Loading user: {u['url']}...")
            self.live_list.append(u)
        log.info(f"Loaded {len(self.live_list)} users in total")

    def assmble_users(self):
        for c in self.live_list:
            _c = self._user_info(c)
            u = User(_c)
            self.users.append(u)
    
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