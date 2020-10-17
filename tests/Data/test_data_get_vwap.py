import quant_sdk as sdk
from quant_sdk import Data

sdk.ApiConfig.api_key = '5mvme03jjsG6E6r36A55yQnDWtpPFMT040P5q0XRs7UuXo29l913eGKepl4B9eBXCrziQXdOyjOwjYbeSMrdynfsQPNUegwptngdfj2bwsnI37yEdfg6c99F1BxxdmxA'

intervals = ['1s', '5s', '30s', '60s', '1m', '5m', '15m', '30m', '1h', '2h', '6h', '12h', '24h']

bases = ['BTC', 'ETH']
quotes = ['USD', 'EUR']

for base in bases:
    for quote in quotes:
        for interval in intervals:
            print(f'{base}{quote} - {interval}')
            print(Data().get_vwap(base=base, quote=quote, interval=interval), '\n')
