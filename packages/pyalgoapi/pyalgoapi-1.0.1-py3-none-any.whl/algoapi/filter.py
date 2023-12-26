import json

from algoapi.base import BaseClient
from algoapi.exceptions import FilterError


class FilterClient(BaseClient):

    def __init__(self) -> None:
        super().__init__()
        self.user_id = None

    def get_filter_range(self):
        endpoint = '/pbapi/api/getFilterRange'

        return self._get(endpoint=endpoint)

    def get_all_filters(self):
        if not isinstance(self.user_id, str):
            raise FilterError(self.user_id)

        endpoint = '/pbapi/api/getFilters'
        headers = {'X-USERNAME': self.user_id}

        return self._get(endpoint=endpoint, headers=headers)

    def get_filter_by_id(self, filter_id: str):
        filter = [
            f for f in self.get_all_filters()['data']
            if f['FilterId'] == int(filter_id)
        ][0]

        return {
            'filter_id': filter_id,
            'name': filter['Name'],
            'exchange': filter['ExchangeCode'],
            'industry': filter['IndustryCode'],
            'filter': json.loads(filter['Criteria'])
        }

    def create_filter(
        self,
        filter: list[dict],
        exchange: str,
        industry: str,
        name: str,
    ):
        return self._filter(
            action='RC',
            filter=filter,
            exchange=exchange,
            industry=industry,
            name=name,
        )

    def run_filter(self, filter: list[dict], exchange: str, industry: str):
        return self._filter(
            action='R',
            filter=filter,
            exchange=exchange,
            industry=industry,
        )

    def run_filter_by_id(self, filter_id):
        filter = self.get_filter_by_id(filter_id)
        filter = {k: filter[k] for k in ['filter', 'exchange', 'industry']}

        return self.run_filter(**filter)

    def update_filter(
        self,
        filter_id: str,
        filter: list[dict],
        exchange: str,
        industry: str,
        name: str,
    ):
        return self._filter(
            action='RU',
            filter_id=filter_id,
            filter=filter,
            exchange=exchange,
            industry=industry,
            name=name
        )

    def delete_filter(self, filter_id: str):
        if not isinstance(self.user_id, str):
            raise FilterError(self.user_id)

        endpoint = '/pbapi/api/deleteFilter'
        headers = {'X-USERNAME': self.user_id}

        return self._post(
            endpoint=endpoint,
            headers=headers,
            data=self._params(self.delete_filter, locals())
        )

    def _filter(
        self,
        action: str,
        filter: list[dict],
        exchange: str,
        industry: str,
        lang: str = 'vi',
        filter_id: str = '8386',
        name: str = '',
    ):
        if not isinstance(self.user_id, str):
            raise FilterError(self.user_id)

        endpoint = '/pbapi/api/filter'
        headers = {'X-USERNAME': self.user_id}
        params = self._params(self._filter, locals())

        return self._post(endpoint=endpoint, headers=headers, data=params)
