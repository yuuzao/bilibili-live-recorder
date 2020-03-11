import sys
import argparse
from pathlib import Path

from live.param import Fpath
from live.log import log


class Cmd:
    def __init__(self):
        self._config_file = [Fpath.config_file]
        self._save_dir = [Fpath.save_dir]

        self.config_file = self._config_file[0]
        self.save_dir = self._save_dir[0]

        self.cmd()

    def __repr__(self):
        c = self.__class__.__name__
        string = f'{c}(config_file:{self._config_file}, save_dir: {self._save_dir})'
        return string

    def cmd(self):
        parser = argparse.ArgumentParser(description="A bilibili live recorder ●REC")
        parser.add_argument(
            "-c",
            "--config",
            metavar="",
            help="location of your live \
                    list, default is '$HOME/.config/livelist.toml'",
        )
        parser.add_argument(
            "-d",
            "--dir",
            metavar="",
            help="directory to save your \
            reording file, default is '$HOME/Videos/bilibili'",
        )
        args = vars(parser.parse_args())

        self._update(self._is_exists, self._config_file, args['config'])
        # self._update(self._mkdir, self._save_dir, args['dir'])
    
    def _update(self, func, target, arg):
        if arg is not None:
            target[0] = Path(arg)
            log.info(f'using custom path: {target}')
        else:
            log.info(f'using default path: {target}')
        func(target[0])

    def _is_exists(self, p):
        if not p.exists():
            log.error(f'"{p}" does not exist, exiting...')
            if exit:
                sys.exit(1)