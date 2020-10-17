
class Signal:

    SIGNAL_TYPES = ('BUY', 'SELL', 'HOLD')

    def __init__(
            self,
            signal_type=None,
            executed_flag=None,
            signal_volume=None,
            market_or_limit=None,
            exchange_list=None
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
