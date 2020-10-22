from typing import Union, List, Any
import pandas as pd
from .api_client import ApiClient
from .util_functions.utils import interval_converter
import requests


class Data:

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_orderbook_data(self, exchanges: Union[str, List[str]], base: str, quote: str, depth: int = 5,
                           range_lb: Union[float, int, str] = None, range_ub: Union[float, int, str] = None) -> Any:

        try:
            if type(exchanges) == list:
                exchanges = ', '.join(exchanges)

            pair = base + quote

            params = {
                'exchanges': exchanges,
                'ticker': pair,
                'limit': depth,
                # 'range': f'{range_lb}, {range_ub}'  # todo fix
            }
            return self.api_client.make_api_call(method='GET', access_route=f'data/orderbook', params=params).json()

        except Exception as ex:
            print(ex)

    def get_vwap(self, base: str, quote: str, interval: Union[str, int]) -> Any:

        try:
            pair = base + quote
            if type(interval) == str:
                interval = interval_converter(interval)
            url_extension = f'data/vwap/latest/{pair}/{interval}'
            return self.api_client.make_api_call(method='GET', access_route=url_extension, params=None).json()
        except Exception as ex:
            print(ex)

    def get_ohlc(self, base: str, quote: str, interval: str) -> Any:

        try:
            pair = base + quote
            if type(interval) == str:
                interval = interval_converter(interval)
            url_extension = f'data/ohlc/latest/{pair}/{interval}'
            return self.api_client.make_api_call(method='GET', access_route=url_extension, params=None).json()
        except Exception as ex:
            print(ex)

    def get_historical_vwap(
            self,
            base: str,
            quote: str,
            interval: str,
            start_date: int,
            end_date: int,
            return_df: bool = True,
            convert_to_datetime: bool = True) -> Union[pd.DataFrame, Any]:

        """
        Returns the json-encoded content of a response, if any.
        :param convert_to_datetime:
        :param return_df:
        :param base: ETH, BTC
        :param quote: EUR, USD
        :param interval:
        :param start_date: timestamp
        :param end_date: timestamp
        :return:
        """

        try:
            pair = base + quote
            if type(interval) == str:
                interval = interval_converter(interval)
            url_extension = f'data/vwap/historic/{pair}/{interval}'
            params = {
                'from': start_date,
                'to': end_date
            }
            response_data = self.api_client.make_api_call(method='GET', access_route=url_extension,
                                                          params=params).json()
            if return_df is False:
                return response_data

            # only if return_df is set to True
            df = pd.DataFrame(response_data)
            if df.empty:
                return df

            if convert_to_datetime is True:
                df.rename(columns={'timestamp': 'Time', 'price': 'Price', 'volume': 'Volume'}, inplace=True)
                df['Time'] = pd.to_datetime(df['Time'], unit='s')
                df.set_index('Time', inplace=True)
            else:
                df.set_index('timestamp', inplace=True)
            return df
        except Exception as ex:
            print(ex)

    def get_historical_ohlc(
            self,
            base: str,
            quote: str,
            interval: str,
            start_date: int,
            end_date: int,
            return_df: bool = True,
            convert_to_datetime: bool = True) -> Union[pd.DataFrame, Any]:

        """
        Returns the json-encoded content of a response, if any.
        :param convert_to_datetime:
        :param return_df:
        :param base: ETH, BTC
        :param quote: EUR, USD
        :param interval: 1s, 5s, 30s, 1m, 5m, 30m, 60m
        :param start_date: Unix timestamp
        :param end_date: Unix timestamp
        :return:
        """

        try:
            pair = base + quote
            if type(interval) == str:
                interval = interval_converter(interval)
            url_extension = f'data/ohlc/historic/{pair}/{interval}'
            params = {
                'from': start_date,
                'to': end_date
            }
            response_data = self.api_client.make_api_call(method='GET', access_route=url_extension,
                                                          params=params).json()
            if return_df is False:
                return response_data

            # only if return_df is set to True
            df = pd.DataFrame(response_data)
            if df.empty:
                return df

            if convert_to_datetime is True:
                df.rename(columns={'timestamp': 'Time', 'price': 'Price', 'volume': 'Volume'}, inplace=True)
                df['Time'] = pd.to_datetime(df['Time'], unit='s')
                df.set_index('Time', inplace=True)
            else:
                df.set_index('timestamp', inplace=True)
            return df
        except Exception as ex:
            print(ex)
