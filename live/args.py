import sys
import argparse
from pathlib import Path

from live.const import Const
from live.log import log


class Cmd:
    def __init__(self):
        self.config_file = [Const.config_file]
        self.save_dir = [Const.save_dir]
        self.cmd()

    def __repr__(self):
        c = self.__class__.__name__
        string = f'{c}(config_file:{self.config_file}, save_dir: {self.save_dir})'
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

        self._update(self._is_exists, self.config_file, args['config'])
        self._update(self._mkdir, self.save_dir, args['dir'])
    
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

    def _mkdir(self, p):
        if not p.exists():
            log.info(f'creating folder at "{p}"')
            p.mkdir(parents=True)