import re
import datetime
import toml
import asyncio
import aiohttp
import requests
from pathlib import Path

from live.log import log


async def req(url):
    h = header(url)
    async with aiohttp.ClientSession() as s:
        async with s.get(url,allow_redirects=True, headers=h) as res:
            code = res.status
            if code >= 400:
                return {'err': True, 'code': code}
            rr = await res.json()
            return {'err': False, 'code': code, 'res': rr}

def sreq(url):
    h = header(url)
    res = requests.get(url, headers=h)
    code = res.status_code
    if code >= 400:
        return {'err': True, 'code': code}
    rr = res.json()
    return {'err': False, 'code':code, 'res': rr}

def naming(dir, prefix, suffix):
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    name = prefix + ts + '.' + suffix

    return dir.joinpath(name)



async def watch(self, slp, func, *args, **kwds):
    while True:
        await func(*args, **kwds)
        await asyncio.sleep(slp)
    

def header(url):
    temp = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    temp['Host'] = url.host

    return temp