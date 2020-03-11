import asyncio

from live.args import Cmd
from live.task import Lives


async def main():
    cmd = Cmd()
    lv = Lives(cmd.config_file, cmd.save_dir)
    await asyncio.gather(lv.watch_config(),
                        lv.watch_lives_staus(),
                        lv.record())

if __name__ == "__main__":
    asyncio.run(main())