# bilibili-live-recoder

## Table of Contents

- [About](#about)
- [Installing](#installing)
- [Usage](#usage)

## About
这是一个使用`asyncio`实现的`bilibili`直播录制工具.


它会监测房间状态, 在直播开始后自动录制.

它也可以同时录制多个直播(默认最高画质, 请注意带宽是否够用).

它会监测配置文件的改动, 可以在任意时间修改配置文件.


## Installing

请保证`Python`版本不低于3.7

```
pip install bilibili-live-recorder
```

## Usage

```
𝅘𝅥𝅮 blr --help
usage: blr [-h] [-c] [-d]

a bilibili live recorder ●REC...

optional arguments:
  -h, --help      show this help message and exit
  -c , --config   location of your live list, default is '$HOME/.config/livelist.toml'
  -d , --dir      directory to save your reording file, default is '$HOME/Videos/bilibili'

```
配置文件使用`toml`格式, 样子如下:
```

[[users]]
# 这里url既可以是主播的个人空间, 也可以是房间
url = "https://space.bilibili.com/2233"

[[users]]
url = "https://live.bilibili.com/6"

```
默认位置位于`$USER/.config/livelist.toml`, 默认录制的视频位于`$USER/Videos/bilibili`


## License
MIT