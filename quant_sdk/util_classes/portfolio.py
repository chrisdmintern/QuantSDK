from typing import Union, Iterable, Tuple, Any
import pandas as pd
from quant_sdk.configs import Configs
import time


class Portfolio:
    """
    Portfolio class is used for Strategies and Backtesting and Performance Tracking
    """

    # _allow_shorts = True  # todo possible future implementation

    def __init__(self, assets: Union[Tuple[str, Union[float, int]],
                                     Iterable[Tuple[str, Union[float, int]]]] = None):
        """

        :param assets:
        """
        self._funds = {}
        self._no_trades = 0
        self._trade_log = pd.DataFrame(columns=['Base', 'Quote', 'Quantity', 'Price', 'Direction', 'Fees'])

        try:
            if assets is not None:
                if type(assets) == tuple:
                    self.add_funds(assets)
                else:
                    for asset in assets:
                        self.add_funds(asset=asset)
        except Exception as ex:
            print(ex, 'could not add funds')

    def get_funds(self, asset):  # are enough funds available to make trade return True or False
        try:
            try:
                return self._funds[asset]
            except KeyError:
                print(f'Asset {asset} not listed in portfolio')
                return 0
        except (TypeError, ValueError, KeyError) as ex:
            raise ex
        except Exception as ex:
            print(ex)
            return 0

    def add_funds(self, asset: Tuple[str, Union[float, int]]):
        try:
            if asset[0] not in self._funds.keys():
                self._funds[asset[0]] = asset[1]
            else:
                self._funds[asset[0]] += asset[1]
        except Exception as ex:
            print(ex, 'could not add funds')

        return self

    def remove_funds(self, asset: Tuple[str, Union[float, int]]):
        """
        asset is a tuple representing a key (asset name) and the quantity e.g. ('BTC', 3) => will reduce the
        BTC-funds in the portfolio by 3. Funds will not be reduced below 0. Portfolio contains 2 BTC and
        pf.remove_funds(('BTC', 3)) is called the remaining funds will be 0 not -1.
        :param asset: tuple
        :return:
        """
        try:
            if asset[0] not in self._funds.keys():
                raise ValueError(f'Asset {asset[0]} not in portfolio')
            else:
                self._funds[asset[0]] -= asset[1]
                if self._funds[asset[0]] < 0:
                    # self._funds[asset[0]] = 0
                    pass
        except Exception as ex:
            print(ex, 'could not add funds')
        return self

    def set_funds(self, asset: Tuple[str, Union[float, int]]):
        self._funds[asset[0]] = asset[1]
        return self

    def portfolio_return(self):
        pass

    def log_trade(self, order_data: Any):
        """
        Json order response will be appended to the _trade_log attribute
        :param order_data: order json response from Blocksize core external Api
        :return:
        """

        base = order_data['order']['base_currency']
        quote = order_data['order']['quote_currency']
        quantity = float(order_data['order']['quantity'])
        fees = float(order_data['trading_fees'])
        avg_execution_price = float(order_data['average_execution_price'])

        direction = Configs.API_ENCODINGS['direction'][order_data['order']['direction']]
        data = [[base, quote, quantity, avg_execution_price, direction, fees]]

        if direction == 'BUY':
            self.add_funds(asset=(base, quantity))
            self.remove_funds(asset=(quote, avg_execution_price * quantity + fees))
        if direction == 'SELL':
            self.remove_funds(asset=(base, quantity))
            self.add_funds(asset=(quote, avg_execution_price * quantity - fees))

        self._trade_log = self._trade_log.append(pd.DataFrame(
            data,
            index=[time.time()],
            columns=self._trade_log.columns))

    def __repr__(self):
        return f'Portfolio({self._funds})'


if __name__ == '__main__':
    pf = Portfolio([('EUR', 3), ('BTC', 3)])
    pf2 = Portfolio(('EUR', 3))
    print(pf2)
    pf.add_funds(('BTC', 3))
    pf.remove_funds(('BTC', 4))
    pf2.set_funds(('ETH', 50))
    print(pf, pf2)
