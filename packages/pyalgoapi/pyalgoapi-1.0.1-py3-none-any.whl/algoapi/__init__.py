from algoapi.filter import FilterClient
from algoapi.signal import SignalClient
from algoapi.tradingview import TradingViewClient


class AlgoAPI(
    FilterClient,
    SignalClient,
    TradingViewClient,
):

    def __init__(
        self,
        base_url: str = 'http://10.21.186.94:80',
        verbose: bool = False,
    ) -> None:
        super().__init__()
        self.base_url = base_url
        self.verbose = verbose

    def set_user_id(self, user_id: str) -> None:
        self.user_id = user_id