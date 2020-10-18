import pandas as pd
from typing import Union
import datetime
import time
from quant_sdk.util_classes.data_types import Signal
from .data import Data
from .trading import Trading
from .api_client import ApiClient


# !HINT! : Look into copy and deepcopy for || referencing objects without creating unnecessary overhead
# !Hint! : "All orders" is not updating in matrix


# todo pure strategy here - BackTesting module/class will provide data and actual testing
# todo create module or class to run strategies
#  potentially portfolio class to incorporate all factors
# !Hint! : Base Strategy Class to be inherited by the different Strategies
class Strategy:
    # moving averages will need more than just one
    # price snapshot to calculate a signal
    _required_data_length = 1

    # todo implement all the necessary tracking and constraints to reflect actual trading scenarios
    # todo implement fees possible input argument for backtesting function input for the
    def __init__(self,
                 interval: Union[int, float],
                 trade_size: Union[int, float] = 10000,
                 portfolio_size: Union[int, float] = 100000, ):
        # set by inputs
        self.portfolio_size = portfolio_size
        self.trade_size = trade_size
        self.interval = interval

        # overview
        self.no_trades = 0
        self.fees_acc = 0  # todo implement correct fee schedule
        self._trade_log = pd.DataFrame(columns=['Base', 'Quote', 'Quantity', 'Price', 'Direction', 'Fees'])
        self._trade_log.index.name = 'timestamp'

    def show_summary(self):
        return {
            'No_trades': self.no_trades,
            'total_fees': self.fees_acc
        }

    @property
    def trade_log(self):
        return self._trade_log


class SimpleStrategy(Strategy):

    def __init__(self, base: str, quote: str, interval: Union[int, float], buy_price: Union[float, int] = None,
                 sell_price: Union[float, int] = None, execute_order_type: str = 'MARKET'):

        super().__init__(interval)

        self._sell_price: float = sell_price
        self._buy_price: float = buy_price
        self.base = base.upper()
        self.quote = quote.upper()
        self.pair = self.base + self.quote

        self.execute_order_type = execute_order_type  # MARKET or ORDER
        self.exchange_list = None  # which exchanges should be used to execute the strategy

    def create_signal(self, price, ):

        # todo BackTesting use tuples of data series as data inputs for function,
        #  allows for multiple data inputs for signal creation
        #  e.g. create Signal Simple needs only one column
        #  and the current timestamp related price for each individual signal
        #  hence only one pd.Series is needed.
        #  More complex signals might be dependant on open and close price and would need two columns of data
        #  -
        #  - ex.:
        #  - >>> BackTesting().backtest(strategy=ohlc_strat, data=(df['open'], df['close']))
        #  -
        #  the above line is the target base implementation for backtesting
        #  also already considering more complex strategies

        signal = Signal()
        # todo portfolio check || do the funds exist to make a trade size trade accordingly
        if price > self._sell_price:
            signal.signal_type = 'SELL'
            return signal
        elif price < self._buy_price:
            signal.signal_type = 'BUY'
            return signal
        else:
            signal.signal_type = 'HOLD'
            return signal

    def run(self, run_duration: int = 120):
        """

        :param run_duration: duration in seconds
        :return:
        """
        start_time = time.time()
        while True:
            current_price = Data().get_vwap(self.base, self.quote, '1s')['price']
            signal = self.create_signal(current_price)
            print(f'{self.pair} is {current_price} - signal: {signal}')

            if signal != 'Hold':
                quantity = self.trade_size / current_price
                if signal == 'SELL':
                    order_data = Trading().simulated_order(self.base, self.quote, 'SELL', quantity, None, True)
                    self.log_order(order_data, 'Sell')

                elif signal == 'BUY':
                    order_data = Trading().simulated_order(self.base, self.quote, 'BUY', quantity, None, True)
                    self.log_order(order_data, 'BUY')

            if (time.time() - start_time) > run_duration:
                break
            time.sleep(self.interval)

    # todo change global (base, quote) to pair
    def backtest(self, start_date, end_date):

        test_data = Data().get_historical_vwap(self.base, self.quote, self.interval, start_date, end_date)
        return test_data

    @property
    def sell_price(self):
        return self._sell_price

    @sell_price.setter
    def sell_price(self, sell_price: Union[float, int]):
        self._sell_price = sell_price

    @property
    def buy_price(self):
        return self._buy_price

    @buy_price.setter
    def buy_price(self, buy_price: Union[float, int]):
        self._buy_price = buy_price

    def log_order(self, order_data, direction):
        data = [[
            order_data['order']['base_currency'],
            order_data['order']['quote_currency'],
            order_data['order']['quantity'],
            order_data['average_execution_price'],
            direction,
            order_data['trading_fees'],
        ]]

        self._trade_log = self._trade_log.append(pd.DataFrame(
            data,
            index=[time.time()],
            columns=self._trade_log.columns))


class SMAStrategy(Strategy):
    pass


class EMAStrategy(Strategy):
    pass


if __name__ == '__main__':
    s_strat = SimpleStrategy('ETH', 'EUR', 10, 2)

    s_strat.buy_price = Data().get_vwap('ETH', 'EUR', '5s')['price'] * 0.999
    s_strat.sell_price = Data().get_vwap('ETH', 'EUR', '5s')['price'] * 1.001

    pass
