from quant_sdk_lite import BlockSize
import pandas as pd
from typing import Union
import datetime
import time


# !Hint! : Base Strategy Class to be inherited by the different Strategies
class Strategy:

    def __init__(self, block: BlockSize,
                 trade_interval: Union[int, float],
                 evaluation_interval: Union[int, float],
                 trade_size: Union[int, float] = 10000,
                 portfolio_size: Union[int, float] = 100000, ):
        # set by inputs
        self.portfolio_size = portfolio_size
        self.trade_size = trade_size
        self.trade_interval = trade_interval
        self.evaluation_interval = evaluation_interval

        self.block = block

        # overview
        self.no_trades = 0
        self.fees_acc = 0
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

    def __init__(self, block: BlockSize, base: str, quote: str, trade_interval: Union[int, float],
                 evaluation_interval: Union[int, float], buy_price: Union[float, int] = None,
                 sell_price: Union[float, int] = None, ):

        super().__init__(block, trade_interval, evaluation_interval)

        self.base = base.upper()
        self.quote = quote.upper()
        self.pair = self.base + self.quote

        self._sell_price: float = sell_price
        self._buy_price: float = buy_price

    def create_signal(self, price):
        assert self._buy_price, 'buy_price is None'
        assert self._sell_price, 'sell_price is None'

        if price > self._sell_price:
            return 'SELL'
        elif price < self._buy_price:
            return 'BUY'
        else:
            return 'HOLD'

    def run(self):
        start_time = time.time()
        while True:
            current_price = self.block.get_vwap(self.base, self.quote, '1s')['price']
            signal = self.create_signal(current_price)
            print(f'{self.pair} is {current_price} - signal: {signal}')

            if signal != 'Hold':
                quantity = self.trade_size / current_price
                if signal == 'SELL':
                    order_data = self.block.post_simulated_order(self.base, self.quote, 'SELL', quantity, None, True)
                    self.log_order(order_data, 'Sell')

                elif signal == 'BUY':
                    order_data = self.block.post_simulated_order(self.base, self.quote, 'BUY', quantity, None, True)
                    self.log_order(order_data, 'BUY')

            if (time.time() - start_time) > 120:
                break
            time.sleep(self.evaluation_interval)

    # todo change global (base, quote) to pair
    def backtest(self, base, quote, interval, start_date,
                 end_date: int = int(datetime.datetime.now().strftime('%s'))):

        test_data = self.block.get_historical_vwap(base, quote, interval, start_date, end_date)



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
    block = BlockSize('5mvme03jjsG6E6r36A55yQnDWtpPFMT040P5q0XRs7UuXo29l913eGKepl4B9'
                      'eBXCrziQXdOyjOwjYbeSMrdynfsQPNUegwptngdfj2bwsnI37yEdfg6c99F1BxxdmxA')

    s_strat = SimpleStrategy(block, 'ETH', 'EUR', 10, 2)

    s_strat.buy_price = block.get_vwap('ETH', 'EUR', '5s')['price'] * 0.999
    s_strat.sell_price = block.get_vwap('ETH', 'EUR', '5s')['price'] * 1.001

    pass
