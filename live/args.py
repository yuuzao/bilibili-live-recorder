import argparse
from pathlib import Path
from live.log import log


def cmd():
    parser = argparse.ArgumentParser(description="A bilibili live recorder ●REC")
    parser.add_argument(
        "-c",
        "--config",
        metavar="",
        help="location of your live \
                list, default is '/home/USER/.config/bilibili-live-list.config'",
    )
    parser.add_argument(
        "-d",
        "--dir",
        metavar="",
        help="directory to save your \
        reording file",
    )
    args = vars(parser.parse_args())

    home = Path.home()
    if args["config"] is None:
        args["config"] = home.joinpath(".config/bilibili-live-list.config")
    if args["dir"] is None:
        live_home = home.joinpath("bilibili")
        if not live_home.exists():
            live_home.mkdir()
        args["dir"] = live_home
    log.info(f"loading config from {args['config']}")
    log.info(f"storage directory is {args['dir']}")
    return args
