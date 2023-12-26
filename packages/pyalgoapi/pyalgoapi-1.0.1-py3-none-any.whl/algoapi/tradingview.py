import datetime as dt

from algoapi.base import BaseClient


class TradingViewClient(BaseClient):

    def get_time(self):
        endpoint = '/tradingview/api/1.1/time'

        return self._get(endpoint=endpoint)

    def get_config(self):
        endpoint = '/tradingview/api/1.1/config'

        return self._get(endpoint=endpoint)

    def get_symbol(self, symbol: str):
        endpoint = '/tradingview/api/1.1/symbols'

        return self._get(
            endpoint=endpoint,
            params=self._params(self.get_symbol, locals()),
        )

    def search_symbols(
        self, query: str, limit: int, type: str, exchange: str = ''
    ):
        endpoint = '/tradingview/api/1.1/search'

        return self._get(
            endpoint=endpoint,
            params=self._params(self.search_symbols, locals())
        )

    def get_history(
        self,
        symbol: str,
        resolution: int | str,
        from_ts: int | dt.datetime,
        to_ts: int | dt.datetime,
    ):
        endpoint = '/tradingview/api/1.1/history'

        return self._get(
            endpoint=endpoint,
            params=self._params(self.get_history, locals()),
        )

    def get_user_charts(self, client: str, user: int, chart: int = None):
        endpoint = '/tradingview/api/1.1/charts'

        return self._get(
            endpoint=endpoint,
            params=self._params(self.get_user_charts, locals())
        )

    def add_user_chart(
        self,
        client: str,
        user: int,  # name has to be unique or API bug
        name: str,
        content: str,
        symbol: str,
        resolution: int | str,
    ):
        endpoint = '/tradingview/api/1.1/charts'
        params = self._params(self.add_user_chart, locals())
        data = {
            k: v
            for k, v in params.items()
            if k in ['name', 'content', 'symbol', 'resolution']
        }
        params = {k: v for k, v in params.items() if k in ['client', 'user']}

        return self._post(
            endpoint=endpoint,
            params=params,
            data=data,
        )

    def delete_user_chart(self, client: str, user: int, chart: int):
        endpoint = '/tradingview/api/1.1/charts'

        return self._delete(
            endpoint=endpoint,
            params=self._params(self.delete_user_chart, locals())
        )
