# --------------------------------------------
import asyncio
import os
import time
from typing import Any, Dict

import aiohttp
import codefast as cf
from codefast.asyncio.rabbitmq import publish
from dotenv import load_dotenv
from rich import print

load_dotenv()
QUEUE = 'custodes'
URL = os.getenv('URL')


# —--------------------------------------------
async def _parse_ip(js: Dict) -> str:
    try:
        masked_ip = '.'.join(js['ip'].split('.')[-1:])
        masked_ip = f'*.*.*.{masked_ip}'
        country = js.get('country', '')
        region = js.get('region', '')
        city = js.get('city', '')
        return f"{country} {region} {city} {masked_ip}"
    except Exception as e:
        import traceback
        cf.error({
            'error': 'parse ip failed',
            'exception': str(e),
            'traceback': traceback.format_exc(),
        })
        return ''


async def ipinfo() -> str:
    fp = '/tmp/ipinfo.json'
    if cf.io.exists(fp):
        ip = await _parse_ip(cf.js(fp))
        if ip:
            return ip
        else:
            # invalue ipinfo file
            cf.io.rm(fp)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://ipinfo.ddot.cc') as resp:
                js = await resp.json()
                cf.js.write(js, fp)
                return await _parse_ip(js)


async def get_service_status(service_name: str, status: Dict[str, Any],
                             expire: int) -> Dict[str, Any]:
    assert isinstance(status, dict), 'status must be dict'
    assert 'code' in status
    assert 'message' in status

    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return {
        'service_name': service_name,
        'status': status,
        'expire': expire,
        'datetime': datetime,
        'ipinfo': await ipinfo()
    }


async def _post_status(service_name: str, status: Dict[str, Any],
                       expire: int) -> Dict[str, Any]:
    js = await get_service_status(service_name, status, expire)

    return await publish(URL, QUEUE, str(js))


async def post(service_name: str,
               status: Dict[str, Any],
               expire: int = 86400,
               loop: bool = False,
               sleep_period=60) -> None:
    while True:
        try:
            js = await _post_status(service_name, status, expire)
            cf.info(js)
            if not loop:
                return js
        except Exception as e:
            import traceback
            cf.error({
                'error': 'post status failed',
                'exception': str(e),
                'traceback': traceback.format_exc(),
            })
            if not loop:
                return None

        await asyncio.sleep(sleep_period)


if __name__ == '__main__':

    async def main():
        print(await post('test', {
            'code': 0,
            'message': 'test'
        },
                         loop=False,
                         sleep_period=3))

    asyncio.run(main())
