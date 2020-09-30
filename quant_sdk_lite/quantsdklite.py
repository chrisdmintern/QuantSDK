import requests
import datetime
import pandas as pd
from typing import Union


class BlockSize:

    def __init__(self, token: str):
        self.token = token

    def get_orderbook_data(self, exchanges: str, base: str, quote: str, depth: int = 1):
        try:
            pair = base + quote
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

    def get_historical_vwap(
            self,
            base: str,
            quote: str,
            interval: str,
            start_date: int,
            end_date: int = int(datetime.datetime.now().strftime('%s'))):

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
            response = requests.get(f"https://api.blocksize.capital/v1/data/vwap/historic/{pair}/"
                                    f"{interval}?from={start_date}&to={end_date}",
                                    headers={"x-api-key": self.token})
            df = pd.DataFrame(response.json())
            if df.empty:
                return df
            df.rename(columns={'timestamp': 'Time', 'price': 'Price', 'volume': 'Volume'}, inplace=True)
            df['Time'] = pd.to_datetime(df['Time'], unit='s')
            df.set_index('Time', inplace=True)
            return df
        except Exception as ex:
            print(ex)

    def get_historic_ohlc(
            self,
            base: str,
            quote: str,
            interval: str,
            start_date: int,
            end_date: int = int(datetime.datetime.now().strftime('%s'))):

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
            if df.empty:
                return df
            df.rename(columns={'timestamp': 'Time',
                               'open': 'Open',
                               'high': 'High',
                               'low': 'Low',
                               'close': 'Close'}, inplace=True)
            df.set_index('Time', inplace=True)

            return df
        except Exception as ex:
            print(ex)

    def post_simulated_order(
            self,
            base: str,
            quote: str,
            direction: str,
            quantity: Union[str, float, int],
            exchange: str = None,
            unlimited_funds: bool = False):

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
            exchange: str = None):

        try:
            if exchange is None:
                pass
            else:
                exchange = exchange.upper()
            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction,
                'Type': 'MARKET',
                'ExchangeList': exchange,
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
