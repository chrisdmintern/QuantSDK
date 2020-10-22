import requests
import pandas as pd
import re
from typing import Union, List, Any
from .api_config import ApiConfig


class BlockSize:

    def __init__(self, token: str = None):
        if token is None:
            token = ApiConfig.api_key
        self.token = token
        self.strategies = {}

    def get_orderbook_data(self, exchanges: Union[str, List[str]], base: str, quote: str, depth: int = 1) -> Any:

        if type(exchanges) == list:
            exchanges = ', '.join(exchanges)
        try:
            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/orderbook?exchanges={exchanges}"
                                    f"&ticker={pair}&limit={depth}", headers={"x-api-key": self.token})
            return response.json()

        except Exception as ex:
            print(ex)

    def get_vwap(self, base: str, quote: str, interval: str) -> Any:

        try:
            pair = base + quote
            response = requests.get(
                f"https://api.blocksize.capital/v1/data/vwap/latest/{pair}/{self.converter(self.converter(interval))}",
                headers={"x-api-key": self.token})
            return response.json()
        except Exception as ex:
            print(ex)

    def get_ohlc(self, base: str, quote: str, interval: str):

        try:
            pair = base + quote
            response = requests.get(
                f"https://api.blocksize.capital/v1/data/ohlc/latest/{pair}/{self.converter(self.converter(interval))}",
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
            end_date: int) -> pd.DataFrame:

        """

        :param base: ETH, BTC
        :param quote: EUR, USD
        :param interval: 1s, 5s, 30s, 1m, 5m, 30m, 60m
        :param start_date: Unix timestamp
        :param end_date: Unix timestamp
        :return:
        """

        try:
            pair = base + quote
            response = requests.get(f"https://api.blocksize.capital/v1/data/vwap/historic/{pair}/"
                                    f"{self.converter(interval)}?from={start_date}&to={end_date}",
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
            end_date: int) -> pd.DataFrame:

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
                                    f"{pair}/{self.converter(interval)}?from={start_date}&to={end_date}",
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
            exchanges: Union[str, List[str]] = None,
            unlimited_funds: bool = False) -> dict:

        try:
            if exchanges is None:
                pass
            else:
                if type(exchanges) == list:
                    exchanges = list(map(lambda exchange: exchange.upper(), exchanges))
                elif type(exchanges) == str:
                    exchanges = exchanges.upper()

            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction.upper(),
                'Type': 'Market',
                'ExchangeList': exchanges,
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
            exchanges: Union[str, List[str]] = None) -> dict:

        try:
            if exchanges is None:
                pass
            else:
                if type(exchanges) == list:
                    exchanges = list(map(lambda exchange: exchange.upper(), exchanges))
                elif type(exchanges) == str:
                    exchanges = exchanges.upper()

            params = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction,
                'Type': 'MARKET',
                'ExchangeList': exchanges,
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

    @staticmethod
    def converter(interval_string: str) -> str:

        try:
            # allows all seconds and interval in respective time-unit
            # allowed: ex. 10m, 600s, 60s, 1m, 2h, 7200s
            # not allowed: ex. 120m, 360m
            # broad sense check of parameters
            assert re.match(r'^[0-5][0-9]?[mh]$|^60[m]$|^[0-9]{1,5}[s]$', interval_string), 'invalid interval pattern'

            if interval_string[-1] == 's':
                return interval_string
            elif interval_string[-1] == 'm':
                return str(f'{int(interval_string[:-1]) * 60}s')
            elif interval_string[-1] == 'h':
                return str(f'{int(interval_string[:-1]) * 60 * 60}s')

        except Exception as ex:
            print(ex)
