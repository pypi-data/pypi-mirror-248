import datetime as dt
import inspect
import json

import requests

from algoapi.exceptions import APIError


class BaseClient:

    def __init__(self) -> None:
        self.client = requests.Session()

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ) -> dict:
        headers = self._merge_headers(headers)

        r = self.client.request(
            method=method,
            url=self.base_url + endpoint,
            params=params,
            data=data,
            headers=headers,
        )

        if self.verbose:
            log = f'{method} {r.url}'
            if (method == 'POST' and data):
                log = f'{log} {data}'
            print(log)

        try:
            if r.status_code == 200:
                return r.json()
            else:
                raise APIError(r)
        except Exception as e:
            print('url:', r.url)
            print('error:', e)

    def _get(self, endpoint, params: dict = None, headers: dict = None) -> dict:
        return self._request('GET', endpoint, params=params, headers=headers)

    def _post(
        self,
        endpoint,
        params: dict = None,
        data: dict = None,
        headers: dict = None
    ) -> dict:
        post_headers = {'Content-Type': 'application/json'}
        data = json.dumps(data)

        if headers:
            post_headers = post_headers | headers

        return self._request(
            'POST', endpoint, params=params, data=data, headers=post_headers
        )

    def _delete(
        self, endpoint, params: dict = None, headers: dict = None
    ) -> dict:
        return self._request('DELETE', endpoint, params=params, headers=headers)

    def _params(self, fn, caller_locals: dict) -> dict:
        params = {}
        # https://docs.python.org/3.8/library/inspect.html#inspect.Signature
        for arg in inspect.signature(fn).parameters.keys():
            val = caller_locals[arg]
            if isinstance(val, dt.datetime):
                val = int(val.timestamp())
            if val is not None:
                if arg.endswith('_ts'):
                    arg = arg.split('_')[0]
                # handle camelCase params of original API
                arg = self._snake_to_camel(arg)

            params[arg] = val

        return params

    def _merge_headers(self, headers: dict = None) -> dict:
        return {
            **headers,
            **self.client.headers
        } if headers else self.client.headers

    @staticmethod
    def _snake_to_camel(snake_str: str) -> str:
        comp = snake_str.split('_')

        camel_str = (comp[0].lower() + ''.join([c.title() for c in comp[1:]]))

        return camel_str.replace('Id', 'ID')
