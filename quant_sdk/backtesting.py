from quant_sdk.strategies import SimpleStrategy, SMAStrategy, EMAStrategy
from typing import Union, Sequence, Tuple, Any
from .util_classes.portfolio import Portfolio
from .api_client import ApiClient
from .data import Data
import pandas as pd
from pandas import DataFrame

import time


class BackTesting:

    def __init__(self,
                 api_client: ApiClient = None):

        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    @staticmethod
    def backtest_custom_data(strategy: Union[SimpleStrategy, SMAStrategy, EMAStrategy],
                             beginning_balance: Union[Tuple[str, Union[float, int]],
                                                      Sequence[Tuple[str, Union[float, int]]]],
                             fees_bp: Union[float, int] = 1.25,
                             buffer_multiplier: Union[float, int] = 4,
                             data: Sequence[Union[Sequence[Any]]] = None) -> Tuple[Portfolio, DataFrame, DataFrame]:

        """
        :param buffer_multiplier:
        :param fees_bp: fees as percentage value e.g. 0.25 => 0.25% => 0.0025
        :param strategy:
        :param data:
        :param beginning_balance: if none function will default to [(strategy.quote, 100000), (strategy.base, 10)]
        :return:
        """

        fees_bp *= 0.01
        fee_buffer = fees_bp * strategy.trade_volume * buffer_multiplier
        if beginning_balance is None:
            beginning_balance = [(strategy.quote, 100000), (strategy.base, 10)]
        total_log = pd.DataFrame(
            columns=[f'BB-{strategy.quote}', f'EB-{strategy.quote}', f'BB-{strategy.base}', f'EB-{strategy.base}',
                     f'Total Value in {strategy.quote}', 'Signal', 'Executed', 'Price', 'Quantity', 'Net Trade Volume',
                     'Fees'])

        pf = Portfolio(beginning_balance)
        pf_log = pd.DataFrame(columns=['Quote', 'Base', f'Total Value in {strategy.quote}', 'Price'])
        pf_log.index.name = 'timestamp'

        pf_total_value = data[0][0] * pf.get_funds(strategy.base) + pf.get_funds(strategy.quote)
        total_log = total_log.append({
            f'BB-{strategy.quote}': pf.get_funds(strategy.quote),
            f'BB-{strategy.base}': pf.get_funds(strategy.base),
            f'Total Value in {strategy.quote}': pf_total_value
        }, ignore_index=True)
        #
        # for row in data:
        #     # todo implement automatic conversion to list if single values are given
        #     fees = 0
        #     signal = strategy.signal_trade(*row)
        #     signal.market_or_limit = 'MARKET'
        #     BB_quote = pf.get_funds(strategy.quote)
        #     BB_base = pf.get_funds(strategy.base)
        #
        #     print(*row, signal)
        #
        #     quote_pf_balance = pf.get_funds(strategy.quote)
        #     base_pf_balance = pf.get_funds(strategy.base)
        #     if signal.signal_type != 'HOLD':
        #         if not (quote_pf_balance > fee_buffer and signal.signal_type == 'BUY'):
        #             # !HINT! : example data relevant fields for trade logging are held dynamic
        #             if signal.signal_type == 'SELL':
        #                 if base_pf_balance < signal.signal_volume:
        #                     signal.signal_volume = base_pf_balance
        #                     fees = signal.signal_volume * row[0] * fees_bp
        #                 direction = 1
        #             elif signal.signal_type == 'BUY':
        #                 if quote_pf_balance < signal.signal_volume * row[0]:
        #                     signal.signal_volume = quote_pf_balance / row[0]
        #                     fees = signal.signal_volume * row[0] * fees_bp
        #                 direction = 2
        #             else:
        #                 raise UserWarning('signal returned something other than BUY, SELL or HOLD')
        #
        #             data = {
        #                 'order': {
        #                     'base_currency': strategy.base,
        #                     'quote_currency': strategy.quote,
        #                     'direction': direction,
        #                     'type': 'MARKET',
        #                     'quantity': signal.signal_volume,
        #                     'bsc_token_id': '3a3aa41a-2ff8-43df-b9f4-956f32990bec',
        #                     'user_id': 'zbzzKcIonNVSctB4Y0JG5qBhdCv2'
        #                 },
        #                 'elapsed_time_retrieval': 64361,
        #                 'elapsed_time_calculation': 2063,
        #                 'average_execution_price': row[0],
        #                 'trading_fees': fees,  # todo mind this
        #                 'trades': [
        #                     {
        #                         'exchange': 'BITFLYER',
        #                         'quantity': '9.353818129999999',
        #                         'apikey_id': '00000000-0000-0000-0000-000000000000',
        #                         'average_execution_price': '10047.796741953993',
        #                         'trading_fees': '187.97052666288835',
        #                         'funds': '-1',
        #                         'fee_bp': '20',
        #                         'trade_id': 'd02e6c76-6490-4710-b9d8-bdd28dba55d5',
        #                         'buffer_bp': '25'
        #                     }
        #                 ]
        #             }
        #
        #             pf.log_trade(order_data=data)
        #             signal.executed_flag = True
        #
        #     # pf summary for current iteration
        #     EB_quote = pf.get_funds(strategy.quote)
        #     EB_base = pf.get_funds(strategy.base)
        #     pf_total_value = row[0] * EB_base + EB_quote
        #     pf_log = pf_log.append({'Quote': EB_quote, 'Base': EB_base,
        #                             f'Total Value in {strategy.quote}': pf_total_value,
        #                             'Price': row[0]},
        #                            ignore_index=True)
        #
        #     total_log = total_log.append(
        #         {f'BB-{strategy.quote}': BB_quote, f'BB-{strategy.base}': BB_base, f'EB-{strategy.quote}': EB_quote,
        #          f'EB-{strategy.base}': EB_base, f'Total Value in {strategy.quote}': pf_total_value,
        #          'Signal': signal.signal_type,
        #          'Price': row[0], 'Quantity': signal.signal_volume, 'Fees': fees}, ignore_index=True)
        #     print(pf)

        for row in data:
            fees = 0
            net_trade_volume = 0
            signal = strategy.signal_trade(*row)
            signal.market_or_limit = 'MARKET'

            print(*row, signal)
            # check for sufficient funds after fee buffer

            direction = 1

            BB_quote = pf.get_funds(strategy.quote)
            BB_base = pf.get_funds(strategy.base)

            move_forward = False

            if signal.signal_type != 'HOLD':
                move_forward = True
                if signal.signal_type == 'SELL':
                    if signal.signal_volume * row[0] < fee_buffer:
                        move_forward = False
                    else:
                        fees = signal.signal_volume * row[0] * fees_bp
                    direction = 1
                elif signal.signal_type == 'BUY':
                    if BB_quote < signal.signal_volume * row[0] + fee_buffer:
                        signal.signal_volume = (BB_quote - fee_buffer) / row[0]
                    else:
                        fees = signal.signal_volume * row[0] * fees_bp
                    direction = 2
                else:
                    raise UserWarning('signal returned something other than BUY, SELL or HOLD')

            if move_forward:
                order_data = {
                    'order': {
                        'base_currency': strategy.base,
                        'quote_currency': strategy.quote,
                        'direction': direction,
                        'type': 'MARKET',
                        'quantity': signal.signal_volume,
                        'bsc_token_id': '3a3aa41a-2ff8-43df-b9f4-956f32990bec',
                        'user_id': 'zbzzKcIonNVSctB4Y0JG5qBhdCv2'
                    },
                    'elapsed_time_retrieval': 64361,
                    'elapsed_time_calculation': 2063,
                    'average_execution_price': row[0],
                    'trading_fees': fees,  # todo mind this
                    'trades': [
                        {
                            'exchange': 'BITFLYER',
                            'quantity': '9.353818129999999',
                            'apikey_id': '00000000-0000-0000-0000-000000000000',
                            'average_execution_price': '10047.796741953993',
                            'trading_fees': '187.97052666288835',
                            'funds': '-1',
                            'fee_bp': '20',
                            'trade_id': 'd02e6c76-6490-4710-b9d8-bdd28dba55d5',
                            'buffer_bp': '25'
                        }
                    ]
                }

                pf.log_trade(order_data=order_data)
                net_trade_volume = signal.signal_volume * row[0]

            EB_quote = pf.get_funds(strategy.quote)
            EB_base = pf.get_funds(strategy.base)
            pf_total_value = row[0] * EB_base + EB_quote
            pf_log = pf_log.append({'Quote': EB_quote, 'Base': EB_base,
                                    f'Total Value in {strategy.quote}': pf_total_value,
                                    'Price': row[0]},
                                   ignore_index=True)

            if net_trade_volume == 0:
                signal.executed_flag = False
            else:
                signal.executed_flag = True

            total_log = total_log.append(
                {f'BB-{strategy.quote}': BB_quote, f'BB-{strategy.base}': BB_base, f'EB-{strategy.quote}': EB_quote,
                 f'EB-{strategy.base}': EB_base, f'Total Value in {strategy.quote}': pf_total_value,
                 'Signal': signal.signal_type, 'Net Trade Volume': net_trade_volume, 'Executed': signal.executed_flag,
                 'Price': row[0], 'Quantity': signal.signal_volume, 'Fees': fees}, ignore_index=True)
            print(pf)

        return pf, pf_log, total_log

    @staticmethod
    def backtest(strategy: Union[SimpleStrategy, SMAStrategy, EMAStrategy],
                 beginning_balance: Union[Tuple[str, Union[float, int]],
                                          Sequence[Tuple[str, Union[float, int]]]] = None,
                 fees_bp: Union[float, int] = 25,
                 buffer_multiplier: Union[float, int] = 4,
                 slippage: Union[float, int] = 10,
                 start_time: int = None,
                 end_time: int = None,
                 time_delta: int = 400):
        """

        :param strategy:
        :param beginning_balance:
        :param fees_bp: fee rate in basis points value e.g. 25 => 0.25% => 0.0025
        :param buffer_multiplier:
        :param slippage: in percent e.g. 5 => 5% => 0.05
        :param start_time:
        :param end_time:
        :param time_delta:
        :return:
        """
        # !HINT! : time_delta only in combination with end_time (start_time is None)

        # !HINT! : set variables
        # todo create slippage-index
        quote = strategy.quote
        base = strategy.base
        interval = strategy.interval

        if end_time is None:
            end_time = int(time.time())
        if start_time is None:
            start_time = end_time - interval * time_delta  # todo testing only change to 400

        if beginning_balance is None:
            beginning_balance = (quote, 100000)

        if fees_bp is None:
            fees_bp = 0
        fees_bp *= 0.0001

        if slippage is None:
            slippage = 0
        slippage *= 0.01
        fee_buffer = fees_bp * strategy.trade_volume * buffer_multiplier

        pf = Portfolio(beginning_balance)

        pf_log = pd.DataFrame(columns=['Quote', 'Base', f'Total Value in {quote}', 'Price'])

        total_log = pd.DataFrame(
            columns=[f'BB-{quote}', f'EB-{quote}', f'BB-{base}', f'EB-{base}',
                     f'Total Value in {quote}', 'Signal', 'Executed', 'Price', 'Quantity', 'Net Trade Volume',
                     'Fees'])

        # !HINT! : fetch backtesting_data
        # todo parallelize call then join threads before joining tables,
        #  important performance improvement for larger data sets
        data_ohlc = Data().get_historical_ohlc(base=base, quote=quote, interval=interval, start_date=start_time,
                                               end_date=end_time, convert_to_datetime=True)
        data_vwap = Data().get_historical_vwap(base=base, quote=quote, interval=interval, start_date=start_time,
                                               end_date=end_time, convert_to_datetime=True)

        data_full = data_ohlc.join(data_vwap)

        pf_total_value = data_full.iloc[0]['Price'] * pf.get_funds(base) + pf.get_funds(quote)

        opening_funds_quote = pf.get_funds(quote)
        opening_funds_base = pf.get_funds(base)

        pf_log.loc[0] = [opening_funds_quote, opening_funds_base, pf_total_value, data_full.iloc[0]['Price']]
        total_log = total_log.append({
            f'BB-{quote}': pf.get_funds(quote),
            f'BB-{base}': pf.get_funds(base),
            f'Total Value in {quote}': pf_total_value
        }, ignore_index=True)

        for index, row in data_full.iterrows():

            price = row['Price']

            BB_quote = pf.get_funds(quote)
            BB_base = pf.get_funds(base)

            fees = 0
            net_trade_volume = 0
            signal = strategy.signal_trade(price=price)
            signal.market_or_limit = 'MARKET'

            move_forward = False

            direction = None

            simulated_execution_price = 0
            if signal.signal_type == 'SELL':
                simulated_execution_price = price * (1 - slippage)
            elif signal.signal_type == 'BUY':
                simulated_execution_price = price * (1 + slippage)

            if signal.signal_type != 'HOLD':
                move_forward = True
                if signal.signal_type == 'SELL':
                    direction = 1
                    if BB_base < signal.signal_volume:
                        signal.signal_volume = BB_base
                elif signal.signal_type == 'BUY':
                    direction = 2
                    if BB_quote < signal.signal_volume * simulated_execution_price + fee_buffer:
                        signal.signal_volume = (BB_quote - fee_buffer) / simulated_execution_price
                else:
                    raise UserWarning('signal returned something other than BUY, SELL or HOLD')

            if move_forward:
                fees = abs(signal.signal_volume * simulated_execution_price * fees_bp)
                order_data = {
                    'order': {
                        'base_currency': base,
                        'quote_currency': quote,
                        'direction': direction,
                        'quantity': signal.signal_volume,
                    },
                    'average_execution_price': simulated_execution_price,
                    'trading_fees': fees,  # todo mind this
                }

                pf.log_trade(order_data=order_data)
                net_trade_volume = signal.signal_volume * simulated_execution_price
            EB_quote = pf.get_funds(quote)
            EB_base = pf.get_funds(base)
            pf_total_value = price * EB_base + EB_quote

            pf_log.loc[index] = [EB_quote, EB_base, pf_total_value, price]
            if net_trade_volume == 0:
                signal.executed_flag = False
            else:
                signal.executed_flag = True

            total_log.loc[index] = [BB_quote, EB_quote, BB_base, EB_base, pf_total_value, signal.signal_type,
                                    signal.executed_flag, price, signal.signal_volume, net_trade_volume, fees]
            print(pf)

        return pf, pf_log, data_full
