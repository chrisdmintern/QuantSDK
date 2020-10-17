
class Configs:
    ORDER_STATES = ('OPEN', 'CLOSED', 'FAILED', 'PARTIALLY_FILLED')
    ORDER_TYPES = ('MARKET', 'LIMIT')
    SIGNAL_TYPES = ('BUY', 'SELL', 'HOLD')
    API_ENCODINGS = {
        'direction': {
            1: 'SELL',
            2: 'BUY'
        },
        'aggregated_status': {
            1: 'OPEN',
            2: 'CLOSED',
            3: 'FAILED',
            4: 'PARTIALLYFILLED'
        },
        'order_type': {
            1: 'MARKET',
            2: 'LIMIT'
        }
    }
