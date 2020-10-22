from quant_sdk.api_client import ApiClient
from typing import Union
from quant_sdk.configs import Configs


class Order:
    _ORDER_STATES = Configs.ORDER_STATES
    _API_ENCODINGS = Configs.API_ENCODINGS
    _ORDER_TYPES = Configs.ORDER_TYPES

    def __init__(self,
                 order_id: str = None,
                 base_currency: str = None,
                 quote_currency: str = None,
                 direction: str = None,
                 quantity: Union[float, int] = None,
                 order_type: str = 'MARKET',
                 update_on_init: bool = False):

        if base_currency is not None:
            base_currency.upper()
        if quote_currency is not None:
            quote_currency.upper()
        if direction is not None:
            direction.upper()
        if order_type is not None:
            order_type.upper()

        self._order_id = order_id
        self._base_currency = base_currency
        self._quote_currency = quote_currency
        self._quantity = quantity
        self._direction = direction
        self._order_type = order_type
        self._status = None
        self._timestamp = None
        self._trade_status = None

        if update_on_init:
            self.order_update()

    # todo does not update the attributes but returns self without changes made to Order
    def order_status(self, original_response: bool = False):
        if original_response:
            return ApiClient().make_api_call(method='GET', access_route=f'trading/orders/id/{self._order_id}').json()
        else:
            return self

    def order_log(self, original_response: bool = False):
        if original_response:
            return ApiClient().make_api_call(method='GET',
                                             access_route=f'trading/orders/id/{self._order_id}/logs').json()
        else:
            return self

    def cancel_order(self):
        raise UserWarning('Cancelling orders is yet to be enabled')

    def order_update(self, original_response: bool = False):
        """
        makes a request and updates the attributes of the Order Object
        :return:
        """
        try:
            data = self.get_order_status(self._order_id)
            self._status = self._API_ENCODINGS['aggregated_status'][data['aggregated_status']]
            self._direction = self._API_ENCODINGS['direction'][data['order']['direction']]
            self._base_currency = data['order']['base_currency']
            self._quote_currency = data['order']['quote_currency']
            self._trade_status = data['trade_status']
            self._timestamp = data['order']['order_timestamp']
            self._quantity = data['order']['quantity']
            self._order_type = self._API_ENCODINGS['order_type'][data['order']['type']]

            if original_response:
                return data
            else:
                return self
        except Exception as ex:
            print(ex)

    def _order_data(self):
        return {
            'order_id': self._order_id,
            'order_type': self._order_type,
            'status': self._status,
            'timestamp': self._timestamp,
            'base_currency': self._base_currency,
            'quote_currency': self._quote_currency,
            'quantity': self._quantity,
            'direction': self._direction,
            'trade_status': self._trade_status,
        }

    @staticmethod
    def get_order_status(order_id):
        return ApiClient().make_api_call(method='GET', access_route=f'trading/orders/id/{order_id}').json()

    def __repr__(self):
        return f"Order({self._order_data()})"


class LimitOrder(Order):
    _limit_price = None  # limit order class extension

    def __init__(self, order_id: str = None, base_currency: str = None, quote_currency: str = None,
                 direction: str = None, quantity: Union[float, int] = None, update_on_init: bool = False):

        super().__init__(order_id, base_currency, quote_currency, direction, quantity, 'LIMIT', update_on_init)

    def order_update(self, original_response: bool = False):
        """
        makes a request and updates the attributes of the Order Object
        :return:
        """
        try:
            data = self.get_order_status(self._order_id)
            self._status = self._API_ENCODINGS['aggregated_status'][data['aggregated_status']]
            self._direction = self._API_ENCODINGS['direction'][data['order']['direction']]
            self._base_currency = data['order']['base_currency']
            self._quote_currency = data['order']['quote_currency']
            self._trade_status = data['trade_status']
            self._timestamp = data['order']['order_timestamp']
            self._quantity = data['order']['quantity']
            self._order_type = self._API_ENCODINGS['order_type'][data['order']['type']]
            self._limit_price = data['order']['limit_price']  # limit order class extension

            if original_response:
                return data
            else:
                return self
        except Exception as ex:
            print(ex)


class SimulatedOrder(Order):
    __simulated = True  # simulated order class extension

    def __init__(self, order_id: str = None, base_currency: str = None, quote_currency: str = None,
                 direction: str = None, quantity: Union[float, int] = None, update_on_init: bool = False):
        super().__init__(order_id, base_currency, quote_currency, direction, quantity, update_on_init=update_on_init)

    def _order_data(self):
        return {
            'order_id': self._order_id,
            'order_type': f'Simulated-{self._order_type}',
            'status': self._status,
            'timestamp': self._timestamp,
            'base_currency': self._base_currency,
            'quote_currency': self._quote_currency,
            'quantity': self._quantity,
            'direction': self._direction,
            'trade_status': self._trade_status,
        }


class SimulatedLimitOrder(SimulatedOrder, LimitOrder):
    # combines the enhancements of SimulatedOrder and LimitOrder class
    def __init__(self, order_id: str = None, base_currency: str = None, quote_currency: str = None,
                 direction: str = None, quantity: Union[float, int] = None, update_on_init: bool = False):
        super().__init__(order_id, base_currency, quote_currency, direction, quantity, update_on_init)
