from ...crypto import Crypto
from ... import exceptions
from ...types import Results
import rubpy

class Builder:
    async def builder(
            self: "rubpy.Client",
            name: str,
            tmp_session: bool = False,
            encrypt: bool = True,
            dict: bool = False, **kwargs,
    ) -> Results:
        if not self.connection.api_url:
            await self.connection.get_dcs()

        request = {
            'input': kwargs.get('input', {}),
            'method': name,
        }

        if self.auth is None:
            self.auth = Crypto.secret(length=32)
            # self._client._logger.info(
            #     'create auth secret', extra={'data': self._client._auth})

        if self.key is None:
            self.key = Crypto.passphrase(self.auth)
            # self._client._logger.info(
            #     'create key passphrase', extra={'data': self._client._key})

        request['client'] = self.DEFAULT_PLATFORM
        if encrypt:
            request = {'data_enc': Crypto.encrypt(request, key=self.key)}

        request['tmp_session' if tmp_session is True else 'auth'] = self.auth if tmp_session is True else Crypto.decode_auth(self.auth)
        request['api_version'] = self.API_VERSION

        if tmp_session == False:
            request['sign'] = Crypto.sign(self.private_key, request['data_enc'])

        result = await self.connection.request(request)
        result = Crypto.decrypt(result,
                                key=self.key)
        status = result['status']
        status_det = result['status_det']
        if status == 'OK' and status_det == 'OK':
            if dict:
                return result['dict']

            result['data']['_client'] = self
            return Results(result['data'])

        raise exceptions(status_det)(result, request=request)