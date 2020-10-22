import pandas as pd
from typing import Union
import time
from quant_sdk.util_classes.data_types import Signal
from quant_sdk.data import Data
# from .trading import Trading
# from .util_classes.portfolio import Portfolio


# !HINT! : Look into copy and deepcopy for || referencing objects without creating unnecessary overhead
# !Hint! : "All orders" is not updating in matrix


# todo pure strategy here - BackTesting module/class will provide data and actual testing
# todo create module or class to run strategies
#  potentially portfolio class to incorporate all factors
# !Hint! : Base Strategy Class to be inherited by the different Strategies

class Strategy:

    def __init__(self,
                 base: str,
                 quote: str,
                 interval: Union[float, int],
                 trade_volume: Union[float, int]):
        self.interval = interval
        self.base = base.upper()
        self.quote = quote.upper()
        self.trade_volume = trade_volume

        self._trade_log = pd.DataFrame(columns=['Base', 'Quote', 'Quantity', 'Price', 'Direction', 'Fees'])
        self._trade_log.index.name = 'timestamp'

    def signal_trade(self, **kwargs):
        pass

    def __repr__(self):
        return f'Strategy(' \
               f'base: {self.base}, ' \
               f'quote: {self.base}, ' \
               f'interval: {self.base}, ' \
               f'trade_volume: {self.trade_volume}' \
               f')'


class SimpleStrategy(Strategy):

    def __init__(self, base: str, quote: str, interval: Union[float, int], buy_price: Union[float, int],
                 sell_price: Union[float, int], trade_volume: Union[float, int]):

        super().__init__(base, quote, interval, trade_volume)
        self.buy_price = buy_price
        self.sell_price = sell_price

    def signal_trade(self, price):
        signal = Signal()

        if price > self.sell_price:
            signal.signal_type = 'SELL'
            signal.signal_volume = (self.trade_volume / price)
        elif price < self.buy_price:
            signal.signal_type = 'BUY'
            signal.signal_volume = (self.trade_volume / price)
        else:
            signal.signal_type = 'HOLD'
        return signal

    def __repr__(self):
        return f'SimpleStrategy(' \
               f'base: {self.base}, ' \
               f'quote: {self.base}, ' \
               f'interval: {self.base}, ' \
               f'buy_price: {self.buy_price}, ' \
               f'sell_price: {self.sell_price}, ' \
               f'trade_volume: {self.trade_volume}' \
               f')'


class SMAStrategy(Strategy):
    pass


class EMAStrategy(Strategy):
    pass


# !HINT! : old Strategy constructions
# class Strategy:
#     # moving averages will need more than just one
#     # price snapshot to calculate a signal
#     _required_data_length = 1  # todo check if needed
#     funds = {}
#     _last_start_time = 0  # used by run function to log file
#
#     # todo implement all the necessary tracking and constraints to reflect actual trading scenarios
#     # todo implement fees possible input argument for backtesting function input for the
#     def __init__(self,
#                  base: str,
#                  quote: str = 'USD',
#                  interval: Union[int, float] = 5,
#                  trade_size: Union[int, float] = 10000,
#                  portfolio_size: Union[int, float] = 100000):
#
#         # set by inputs
#         self.trade_size = trade_size
#         self.interval = interval
#         self.base = base.upper()
#         self.quote = quote.upper()
#
#         if portfolio_size and quote:
#             self.initialize_portfolio(base_currency=quote, portfolio_size=portfolio_size)
#
#         # todo fix base_currency ambiguity
#         self.base_currency = quote
#         # overview
#         self.no_trades = 0
#         self.fees_acc = 0  # todo implement correct fee schedule
#         self._trade_log = pd.DataFrame(columns=['Base', 'Quote', 'Quantity', 'Price', 'Direction', 'Fees'])
#         self._trade_log.index.name = 'timestamp'
#
#     # todo improve this function or merge with related methods and remove this method
#     def show_summary(self):
#         return {
#             'No_trades': self.no_trades,
#             'total_fees': self.fees_acc
#         }
#
#     @property
#     def trade_log(self):
#         return self._trade_log
#
#     def initialize_portfolio(self, base_currency, portfolio_size):
#         self.edit_portfolio_assets(base_currency, portfolio_size)
#         self.edit_portfolio_assets(self.base, 0)
#
#     # todo type hinting
#     def edit_portfolio_assets(self, asset, quantity):
#         if asset in self.funds.keys():
#             self.funds[asset] += quantity
#             if quantity > 0:
#                 print(f'{quantity} {asset} were added to the portfolio')
#             else:
#                 print(f'{abs(quantity)} {asset} were removed from the portfolio')
#         else:
#             self.funds[asset] = quantity
#
#     def log_order(self, order_data, direction):
#         # todo make volumes directional -10000 for sell  +10000 for buy
#         #  => easier calculation less ifs ex.: funds += -10000 instead of if buy funds - 10000 or vice versa
#         base = order_data['order']['base_currency']
#         quote = order_data['order']['quote_currency']
#         quantity = float(order_data['order']['quantity'])
#         fees = float(order_data['trading_fees'])
#         avg_execution_price = float(order_data['average_execution_price'])
#
#         data = [[base, quote, quantity, avg_execution_price, direction, fees]]
#         # todo fix portfolio tracking not tracking buys and sells in the balance/funds correctly
#         # todo build proper logging feature
#
#         # f = open('test_logs/trade_logging_2.txt', "a")
#         # f.write(f'{time.time()}---{data}\n')
#         # f.close()
#
#         # print(f'Pre trade funds:\n '
#         #       f'{self.funds[self.base_currency]} {self.base_currency}\n '
#         #       f'{self.funds[self.base]} {self.base}\n')
#         self.no_trades += 1
#         self.fees_acc += fees
#         if direction == 'BUY':
#             self.funds[self.base_currency] -= quantity * avg_execution_price - fees
#             self.funds[self.base] += quantity
#         if direction == 'SELL':
#             self.funds[self.base_currency] += quantity * avg_execution_price - fees
#             self.funds[self.base] -= quantity
#
#         self._trade_log = self._trade_log.append(pd.DataFrame(
#             data,
#             index=[time.time()],
#             columns=self._trade_log.columns))
#
#         f = open(f'test_logs/log_{self._last_start_time}.csv', "a")
#         f.write(f'{time.time()},'
#                 f'{round(self.funds[self.base_currency], 4)},'
#                 f'{self.base_currency},'
#                 f'{round(self.funds[self.base], 6)},'
#                 f'{self.base},'
#                 f'{base + quote},'
#                 f'{direction},'
#                 f'{quantity},'
#                 f'{avg_execution_price},'
#                 f'{fees}'
#                 f'\n'
#                 )
#         f.close()
#         # print(f'After Trade funds: \n '
#         #       f'{self.funds[self.base_currency]} {self.base_currency}\n '
#         #       f'{self.funds[self.base]} {self.base}\n')
#
#
# class SimpleStrategy(Strategy):
#
#     def __init__(self,
#                  base: str,
#                  quote: str,
#                  interval: Union[int, float],
#                  trade_size: Union[int, float] = 10000,
#                  portfolio_size: Union[int, float] = 100000,
#                  buy_price: Union[float, int] = None,
#                  sell_price: Union[float, int] = None,
#                  execute_order_type: str = 'MARKET'):
#
#         super().__init__(base=base,
#                          quote=quote,
#                          interval=interval,
#                          trade_size=trade_size,
#                          portfolio_size=portfolio_size)
#
#         self._buy_price: float = buy_price
#         self._sell_price: float = sell_price
#         self.pair = self.base + self.quote
#
#         self.execute_order_type = execute_order_type  # MARKET or ORDER
#         self.exchange_list = None  # which exchanges should be used to execute the strategy
#
#     def create_signal(self, price: Union[float, int], ) -> Signal:
#
#         # todo BackTesting use tuples of data series as data inputs for function,
#         #  allows for multiple data inputs for signal creation
#         #  e.g. create Signal Simple needs only one column
#         #  and the current timestamp related price for each individual signal
#         #  hence only one pd.Series is needed.
#         #  More complex signals might be dependant on open and close price and would need two columns of data
#         #  -
#         #  - ex.:
#         #  - >>> BackTesting().backtest(strategy=ohlc_strat, data=(df['open'], df['close']))
#         #  -
#         #  the above line is the target base implementation for backtesting
#         #  also already considering more complex strategies
#
#         signal = Signal()
#         # todo portfolio check || do the funds exist to make a trade size trade accordingly
#         if price > self._sell_price:
#             if self.funds[self.base] > 0:
#                 signal.signal_type = 'SELL'
#
#                 if self.funds[self.base] > (self.trade_size / price):
#                     signal.signal_volume = (self.trade_size / price)
#                     return signal
#                 else:
#                     signal.signal_volume = self.funds[self.base]
#                     return signal
#             signal.signal_type = 'HOLD'
#             print(f'Insufficient Funds : {self.base}')
#             return signal
#         elif price < self._buy_price:
#             if self.funds[self.base_currency] > self.trade_size:
#                 signal.signal_type = 'BUY'
#                 signal.signal_volume = (self.trade_size / price)
#                 return signal
#             else:
#                 signal.signal_type = 'Hold'
#                 print(f'Insufficient Funds : {self.base_currency}')
#                 return signal
#         else:
#             signal.signal_type = 'HOLD'
#             return signal
#         # return signal
#
#     def create_signal2(self, price: Union[float, int], pf: Portfolio) -> Signal:
#
#         signal = Signal()
#         # todo portfolio check || do the funds exist to make a trade size trade accordingly
#         if price > self._sell_price:
#             if pf.query_funds(self.base) > 0:
#                 signal.signal_type = 'SELL'
#
#                 if pf.query_funds(self.base) > (self.trade_size / price):
#                     signal.signal_volume = (self.trade_size / price)
#                     return signal
#                 else:
#                     signal.signal_volume = pf.query_funds(self.base)
#                     return signal
#             signal.signal_type = 'HOLD'
#             print(f'Insufficient Funds : {self.base}')
#             return signal
#         elif price < self._buy_price:
#             avail_funds = pf.query_funds(self.base_currency)
#             if avail_funds > self.trade_size:
#                 signal.signal_type = 'BUY'
#                 signal.signal_volume = (self.trade_size / price)
#                 return signal
#             else:
#                 signal.signal_type = 'Hold'
#                 print(f'Insufficient Funds : {self.base_currency}')
#                 return signal
#         else:
#             signal.signal_type = 'HOLD'
#             return signal
#         # return signal
#
#     def run(self, run_duration: int = 120):
#         """
#
#         :param run_duration: duration in seconds
#         :return:
#         """
#         start_time = time.time()
#         self._last_start_time = str(start_time).replace('.', '')
#         while True:
#             current_price = Data().get_vwap(self.base, self.quote, '1s')['price']
#             signal = self.create_signal(current_price)
#             print(f'{self.pair} is {current_price} - signal: {signal.signal_type}')
#
#             if signal.signal_type != 'Hold':
#                 quantity = signal.signal_volume
#                 if signal.signal_type == 'SELL':
#                     order_data = Trading().simulated_order(self.base, self.quote, 'SELL', quantity, None, True)
#                     self.log_order(order_data, 'SELL')
#
#                 elif signal.signal_type == 'BUY':
#                     order_data = Trading().simulated_order(self.base, self.quote, 'BUY', quantity, None, True)
#                     self.log_order(order_data, 'BUY')
#
#             if (time.time() - start_time) > run_duration:
#                 current_price = Data().get_vwap(self.base, self.quote, '1s')['price']
#                 base_value = current_price * self.funds[self.base]
#                 print('\n')
#                 print('\n')
#                 print(f'Portfolio value: \n'
#                       f' {self.funds[self.base_currency]} {self.base_currency} \n'
#                       f' {base_value} {self.base_currency} \n'
#                       f' --------------------------------- \n'
#                       f' {round(base_value + self.funds[self.base_currency])} {self.base_currency}')
#
#                 break
#             time.sleep(self.interval)
#
#     # todo change globally (base, quote) to pair
#     # todo omit this
#     def backtest(self, start_date, end_date):
#
#         test_data = Data().get_historical_vwap(self.base, self.quote, self.interval, start_date, end_date)
#         return test_data
#
#     @property
#     def sell_price(self):
#         return self._sell_price
#
#     @sell_price.setter
#     def sell_price(self, sell_price: Union[float, int]):
#         self._sell_price = sell_price
#
#     @property
#     def buy_price(self):
#         return self._buy_price
#
#     @buy_price.setter
#     def buy_price(self, buy_price: Union[float, int]):
#         self._buy_price = buy_price
#
#
# class SMAStrategy(Strategy):
#     def create_signal(self, price_5: Union[float, int], price_15: Union[float, int]):
#         pass
#
#
# class EMAStrategy(Strategy):
#     def create_signal(self, price, ) -> Signal:
#         pass


if __name__ == '__main__':
    s_strat = SimpleStrategy(base='ETH', quote='EUR', interval=5, buy_price=300, sell_price=400, trade_volume=10000)

    # ema_strat = EMAStrategy(base='ETH', quote='EUR', interval=1, )
    print(s_strat)
    s_strat.buy_price = Data().get_vwap('ETH', 'EUR', '5s')['price'] * 0.999
    s_strat.sell_price = Data().get_vwap('ETH', 'EUR', '5s')['price'] * 1.001

    print(s_strat)
    pass
