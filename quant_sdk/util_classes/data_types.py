from typing import Union, List
from quant_sdk.configs import Configs


class Signal:
    SIGNAL_TYPES = Configs.SIGNAL_TYPES

    def __init__(
            self,
            signal_type: str = None,
            executed_flag: bool = False,
            signal_volume: Union[float, int] = None,
            market_or_limit: str = None,
            exchange_list: List[str] = None
    ):
        self.signal_type = signal_type
        self.executed_flag = executed_flag
        self.signal_volume = signal_volume
        self.market_or_limit = market_or_limit
        self.exchange_list = exchange_list

    def __repr__(self):
        return f'Signal(' \
               f'signal_type: {repr(self.signal_type)}, ' \
               f'executed_flag: {repr(self.executed_flag)}, ' \
               f'signal_volume: {repr(self.signal_volume)}, ' \
               f'market_or_limit: {repr(self.market_or_limit)}, ' \
               f'exchange_list: {repr(self.exchange_list)})'


if __name__ == '__main__':
    print(Signal())
