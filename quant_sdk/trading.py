from .api_client import ApiClient
from .configs import Configs
from typing import Union, Any, List


# !Hint! : ask about orders not being updated
class Trading:

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def market_order(self,
                     base: str,
                     quote: str,
                     direction: str,
                     quantity: Union[str, float, int],
                     exchanges: Union[str, List[str]] = None) -> Any:

        """
        Returns the json-encoded content of a response, if any.
        """
        try:
            if exchanges is None:
                pass
            else:
                if type(exchanges) == list:
                    exchanges = list(map(lambda exchange: exchange.upper(), exchanges))
                elif type(exchanges) == str:
                    exchanges = exchanges.upper()

            data = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction,
                'Type': 'MARKET',
                'ExchangeList': exchanges,
            }

            url_extension = f'trading/orders'
            return self.api_client.make_api_call(method='POST', access_route=url_extension, data=data).json()

        except Exception as ex:
            print(ex)

    def limit_order(self,
                    base: str,
                    quote: str,
                    direction: str,
                    quantity: Union[str, float, int],
                    limit_price: Union[str, float, int],
                    exchanges: Union[str, List[str]] = None) -> Any:
        """
        Returns the json-encoded content of a response, if any.
        """

        try:
            if exchanges is None:
                pass
            else:
                if type(exchanges) == list:
                    exchanges = list(map(lambda exchange: exchange.upper(), exchanges))
                elif type(exchanges) == str:
                    exchanges = exchanges.upper()

            data = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Quantity': quantity,
                'Direction': direction,
                'Type': 'Limit',
                'LimitPrice': limit_price,
                'ExchangeList': exchanges,
            }

            url_extension = f'trading/orders'
            return self.api_client.make_api_call(method='POST', access_route=url_extension, data=data).json()

        except Exception as ex:
            print(ex)

    def simulated_order(self,
                        base: str,
                        quote: str,
                        direction: str,
                        quantity: Union[str, float, int],
                        exchanges: Union[str, List[str]] = None,
                        unlimited_funds: bool = False,
                        disable_logging=False) -> Any:
        """
        Returns the json-encoded content of a response, if any.
        """
        try:
            if exchanges is None:
                pass
            else:
                if type(exchanges) == list:
                    exchanges = list(map(lambda exchange: exchange.upper(), exchanges))
                elif type(exchanges) == str:
                    exchanges = exchanges.upper()

            data = {
                'BaseCurrency': base.upper(),
                'QuoteCurrency': quote.upper(),
                'Direction': direction.upper(),
                'Quantity': quantity,
                'ExchangeList': exchanges,
                'Unlimited': unlimited_funds,
                'Type': 'Market',
                'DisableLogging': disable_logging,
            }
            url_extension = f'trading/orders/simulated'
            return self.api_client.make_api_call(method='POST', access_route=url_extension, data=data).json()
        except Exception as ex:
            print(ex)

    def get_orders(self) -> Any:
        """
        Returns the json-encoded content of a response, if any.    
        """
        try:
            url_extension = f'trading/orders'
            return self.api_client.make_api_call(method='GET', access_route=url_extension).json()
        except Exception as ex:
            print(ex)

    def get_orders_by_status(self, status: str) -> Any:
        """
        Returns the json-encoded content of a response, if any.
        possible order states ('OPEN', 'CLOSED', 'FAILED', 'PARTIALLY_FILLED')
        :raises ValueError - if status argument does not match any of the possible order states
        """
        if status.upper() not in Configs.ORDER_STATES:
            raise ValueError(
                'status argument does not match any of the possible order states; '
                '(OPEN, CLOSED, FAILED, PARTIALLY_FILLED)')
        try:
            url_extension = f'trading/orders/status/{status.upper()}'
            return self.api_client.make_api_call(method='GET', access_route=url_extension).json()
        except Exception as ex:
            print(ex)

    def order_status(self, order_id: str) -> Any:
        """
        Returns the json-encoded content of a response, if any.
        """

        try:
            url_extension = f'trading/orders/id/{order_id}'
            return self.api_client.make_api_call(method='GET', access_route=url_extension).json()
        except Exception as ex:
            print(ex)

    def cancel_order(self, order_id: str) -> Any:
        # """
        # Returns the json-encoded content of a response, if any.
        # """
        # 
        # try:
        #     url_extension = f'trading/orders/id/{order_id}/cancel'  # !Hint! : /cancel is a placeholder
        #     return self.api_client.make_api_call(method='GET', access_route=url_extension).json()
        # except Exception as ex:
        #     print(ex)
        pass
