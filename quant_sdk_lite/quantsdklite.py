import requests
import datetime
import pandas as pd
from typing import Union, Iterable


class BlockSize:

    def __init__(self, token: str):
        self.token: str = token

    def get_orderbook_data(self, exchanges: str, base: str, quote: str, depth: int = 1):
        try:
            pair: str = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/orderbook?exchanges={exchanges}"
                                    f"&ticker={pair}&limit={depth}", headers={"x-api-key": self.token})

            return response.json()

        except Exception as ex:
            print(ex)

    def get_vwap(self, base: str, quote: str, interval: str):

        try:
            pair = base + quote
            response = requests.get(
                f"https://api.blocksize.capital/v1/data/vwap/latest/{pair}/{interval}",
                headers={"x-api-key": self.token})
            return response.json()
        except Exception as ex:
            print(ex)

    def get_ohlc(self, base: str, quote: str, interval: str):

        try:
            pair = base + quote
            response = requests.get(
                f"https://api.blocksize.capital/v1/data/ohlc/latest/{pair}/{interval}",
                headers={"x-api-key": self.token})
            return response.json()
        except Exception as ex:
            print(ex)

    def get_historical_vwap(self, base: str, quote: str, interval: str, start_date: str, end_date: str):

        try:
            start_time_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            start_timestamp = start_time_obj.strftime('%s')
            end_time_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            end_timestamp = end_time_obj.strftime('%s')
            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/vwap/historic/{pair}/"
                                    f"{interval}?from={start_timestamp}&to={end_timestamp}",
                                    headers={"x-api-key": self.token})
            df = pd.DataFrame(response.json())
            df.rename(columns={'timestamp': 'Time', 'price': 'Price', 'volume': 'Volume'}, inplace=True)
            df['Time'] = pd.to_datetime(df['Time'], unit='s')
            df.set_index('Time', inplace=True)
            return df
        except Exception as ex:
            print(ex)

    def get_historic_ohlc(self, base: str, quote: str, interval: str, start_date: int, end_date: int) -> pd.DataFrame:
        """

        :param base: ETH, BTC
        :param quote: EUR, USD
        :param interval:
        :param start_date: Unix time stamp
        :param end_date: Unix time stamp
        :return:
        """

        try:

            pair = base + quote

            response = requests.get(f"https://api.blocksize.capital/v1/data/ohlc/historic/"
                                    f"{pair}/{interval}?from={start_date}&to={end_date}",
                                    headers={"x-api-key": self.token})
            df = pd.DataFrame(response.json())
            df.rename(columns={'timestamp': 'Timestamp',
                               'open': 'Open',
                               'high': 'High',
                               'low': 'Low',
                               'close': 'Close'}, inplace=True)
            df.set_index('Time', inplace=True)

            return df
        except Exception as ex:
            print(ex)

    def post_simulated_order(self, base: str, quote: str, direction: str, quantity: Union[str, float, int],
                             exchange: str = None, unlimited_funds: bool = False):

        if direction.upper() not in ['SELL', 'BUY']:
            print('Direction can only be BUY or SELL as string')
            return
        try:
            if exchange is None:
                pass
            else:
                exchange = exchange.upper()
            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction.upper(),
                'Type': 'Market',
                'ExchangeList': exchange,
                'Unlimited': unlimited_funds,
            }

            response = requests.post("https://api.blocksize.capital/v1/trading/orders/simulated", data=params,
                                     headers={"x-api-key": self.token})
            return response.json()
        except Exception as ex:
            print(ex)

    def post_market_order(
            self,
            base: str,
            quote: str,
            direction: str,
            quantity: Union[str, float, int],
            order_type: int = 0,
            exchange: str = None):

        if direction.upper() not in ['SELL', 'BUY']:
            print('Direction can only be BUY or SELL as string')
            return
        if order_type == (0 or 1) and not exchange:
            print('For Market and Limit orders please select one or multiple exchanges. In case u want to ')

        try:
            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction,
                'Type': 'MARKET',
                'ExchangeList': exchange.upper(),
            }

            response = requests.post("https://api.blocksize.capital/v1/trading/orders?", data=params,
                                     headers={"x-api-key": self.token})

            return response.json()
        except Exception as ex:
            print(ex)

    def order_status(self, order_id: str):

        try:
            response = requests.get(f"https://api.blocksize.capital/v1/trading/orders/id/{order_id}",
                                    headers={"x-api-key": self.token})
            return response.json()

        except Exception as ex:
            print(ex)

    def order_logs(self, order_id: str):

        try:
            response = requests.get(f'https://api.blocksize.capital/v1/trading/orders/id/{order_id}/logs',
                                    headers={"x-api-key": self.token})
            return response.json()
        except Exception as ex:
            print(ex)

    def get_exchange_balances(self):

        try:
            response = requests.get('https://api.blocksize.capital/v1/positions/exchanges',
                                    headers={"x-api-key": self.token})
            return response.json()
        except Exception as ex:
            print(ex)
