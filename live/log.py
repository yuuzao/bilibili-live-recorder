from loguru import logger as log
import sys

log.remove()

log.add(
    sink="err.log",
    level="ERROR",
    format="{time:YYYY/MM/DD-HH:mm:ss} -- {message}"
)

log.add(
    sys.stdout,
    colorize=True,
    format="{time:YYYY/MM/DD@HH:mm:ss} -- <green>{message}</green>"
    )