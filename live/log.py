from loguru import logger as log
import sys

from live.param import Fpath

log.remove()

log.add(
    sink=Fpath.errlog,
    level="ERROR",
    format="{time:YYYY/MM/DDTHH:mm:ss} -- {message}"
)

log.add(
    sink=Fpath.info,
    level="DEBUG",
    format="{time:YYYY/MM/DDTHH:mm:ss} -- {message}"
)
log.add(
    sys.stdout,
    colorize=True,
    format="{time:YYYY/MM/DDTHH:mm:ss} <green>{message}</green>"
    )