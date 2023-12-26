from algoapi.base import BaseClient


class SignalClient(BaseClient):

    def __init__(self) -> None:
        super().__init__()

    def get_formula_signal(self):
        endpoint = '/pbapi/api/formula'

        return self._get(endpoint=endpoint)

    def get_signals(self):
        if not isinstance(self.user_id, str):
            raise SignalError(self.user_id)

        endpoint = '/pbapi/api/signals/' + self.user_id

        return self._get(endpoint=endpoint)

    def get_signals_by_status(self, active: bool):
        signals = self.get_signals()['data']['signals']

        return [signal for signal in signals if signal['active'] == active]

    def _modify_signal(
        self, realtime_formula_id: int, active: bool, user_id=''
    ):
        if not isinstance(self.user_id, str):
            raise SignalError(self.user_id)

        endpoint = '/pbapi/api/signals/' + self.user_id

        return self._post(
            endpoint=endpoint, data=self._params(self._modify_signal, locals())
        )

    def register_signal(self, formula_id: int):
        return self._modify_signal(realtime_formula_id=formula_id, active=True)

    def unsubcribe_signal(self, formula_id: int):
        return self._modify_signal(realtime_formula_id=formula_id, active=False)

    def get_signal_histories(self, formula_id: int):
        if not isinstance(self.user_id, str):
            raise SignalError(self.user_id)

        endpoint = '/pbapi/api/signals/histories/' + self.user_id

        return self._get(
            endpoint=endpoint,
            params=self._params(self.get_signal_histories, locals())
        )
