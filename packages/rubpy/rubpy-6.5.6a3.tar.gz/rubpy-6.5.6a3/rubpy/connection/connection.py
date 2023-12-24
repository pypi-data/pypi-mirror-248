from ..crypto import Crypto
from .. import exceptions
from ..types import Results
import aiohttp
import aiofiles
import asyncio
import os

def capitalize(text: str):
    return ''.join([c.title() for c in text.split('_')])


class Connection:
    def __init__(self, client) -> None:
        self.client = client
        self.session = self.make_session()
        self.api_url = None
        self.wss_url = None

    def make_session(self):
        return aiohttp.ClientSession(
            headers={'user-agent': self.client.user_agent,
            	'origin': 'https://web.rubika.ir',
            	'referer': 'https://web.rubika.ir/'},
            timeout=aiohttp.ClientTimeout(total=self.client.timeout)
        )

    async def close(self):
        await self.session.close()

    async def get_dcs(self):
        try_count = 0

        while True:
            try:
                async with self.session.get('https://getdcmess.iranlms.ir/', verify_ssl=False) as response:
                    if not response.ok:
                        continue

                    response = (await response.json()).get('data')

                self.api_url = response.get('API').get(response.get('default_api'))
                self.wss_url = response.get('socket').get(response.get('default_socket'))
                return True

            except aiohttp.ServerTimeoutError:
                try_count += 1
                print(f'Server timeout error ({try_count})')
                await asyncio.sleep(try_count)
                continue

            except aiohttp.ClientConnectionError:
                try_count += 1
                print(f'Client connection error ({try_count})')
                await asyncio.sleep(try_count)
                continue

    async def request(self, data: dict):
        try_count = 0

        while True:
            try:
                async with self.session.post(self.api_url, json=data, verify_ssl=False) as response:
                    if not response.ok:
                        continue

                    return (await response.json()).get('data_enc')

            except aiohttp.ServerTimeoutError:
                try_count += 1
                print(f'Server timeout error ({try_count})')
                await asyncio.sleep(try_count)
                continue

            except aiohttp.ClientConnectionError:
                try_count += 1
                print(f'Client connection error ({try_count})')
                await asyncio.sleep(try_count)
                continue

    async def update_handler(self, update: dict):
        data_enc: str = update.get('data_enc')

        if data_enc:
            result = Crypto.decrypt(data_enc, key=self.client.key)
            user_guid = result.pop('user_guid')

            for name, package in result.items():
                if not isinstance(package, list):
                    continue

                for update in package:
                    update['client'] = self.client
                    update['user_guid'] = user_guid

                for func, handler in self.client.handlers.items():
                    try:
                        # if handler is empty filters
                        if isinstance(handler, type):
                            handler = handler()

                        if handler.__name__ != capitalize(name):
                            continue

                        # analyze handlers
                        if not await handler(update=update):
                            continue

                        await func(handler)

                    except exceptions.StopHandler as error:
                        print(error.message)
                        break

                    except Exception as error:
                        print(error)
                        # self._client._logger.error(
                        #     'handler raised an exception', extra={'data': update}, exc_info=True)

    async def get_updates(self):
        try_count = 0

        while True:
            try:
                async with self.session.ws_connect(self.wss_url, verify_ssl=False) as wss:
                    self.ws_connect = wss
                    await self.send_json_to_ws()
                    asyncio.create_task(self.send_json_to_ws(data=True))

                    if try_count != 0:
                        print('The connection was re-established.')

                    async for message in wss:
                        if message.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                            await self.send_json_to_ws()

                        message = message.json()
                        asyncio.create_task(self.update_handler(message))

            except aiohttp.ClientConnectionError:
                try_count += 1
                print(f'Client connection error ({try_count})')
                await asyncio.sleep(try_count)

            except ConnectionResetError:
                try_count += 1
                print(f'Connection reset error ({try_count})')
                await asyncio.sleep(try_count)

    async def send_json_to_ws(self, data=False):
        if data:
            while True:
                #try:
                await asyncio.sleep(10)
                await self.ws_connect.send_json('{}')

        return await self.ws_connect.send_json(
            {
                'method': 'handShake',
                'auth': self.client.auth,
                'api_version': '5',
                'data': '',
            })

    async def upload_file(self, file, mime: str = None, file_name: str = None, chunk: int = 1048576 * 2,
                          callback=None, *args, **kwargs):
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError('file not found in the given path')

            if file_name is None:
                file_name = os.path.basename(file)

            async with aiofiles.open(file, 'rb') as file:
                file = await file.read()

        elif not isinstance(file, bytes):
            raise TypeError('file arg value must be file path or bytes')

        if file_name is None:
            raise ValueError('the file_name is not set')

        if mime is None:
            mime = file_name.split('.')[-1]

        result = await self.client.request_send_file(file_name, len(file), mime)

        id = result.id
        index = 0
        dc_id = result.dc_id
        total = int(len(file) / chunk + 1)
        upload_url = result.upload_url
        access_hash_send = result.access_hash_send

        while index < total:
            data = file[index * chunk: index * chunk + chunk]
            try:
                result = await self.session.post(
                    upload_url,
                    headers={
                        'auth': self.client.auth,
                        'file-id': id,
                        'total-part': str(total),
                        'part-number': str(index + 1),
                        'chunk-size': str(len(data)),
                        'access-hash-send': access_hash_send
                    },
                    data=data
                )
                result = await result.json()
                if callable(callback):
                    try:
                        await callback(len(file), index * chunk)

                    except exceptions.CancelledError:
                        return None

                    except Exception:
                        pass

                index += 1
            except Exception:
                pass

        status = result['status']
        status_det = result['status_det']

        if status == 'OK' and status_det == 'OK':
            result = {
                'mime': mime,
                'size': len(file),
                'dc_id': dc_id,
                'file_id': id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']
            }

            return Results(result)

        #self._client._logger.debug('upload failed', extra={'data': result})
        raise exceptions(status_det)(result, request=result)