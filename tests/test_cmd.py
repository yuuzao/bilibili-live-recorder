import pytest

from live.param import Config
from live.args import Cmd


def test_cmd(mocker):
    mocker.patch('sys.argv')
    my_path = Cmd()

    assert my_path.config_file == Config.config_file
    assert my_path.save_dir == Config.save_dir
