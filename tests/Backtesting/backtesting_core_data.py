import quant_sdk as sdk
from quant_sdk import SimpleStrategy, ApiConfig, BackTesting
import matplotlib.pyplot as plt

# !HINT! : most interesting things to look at:
#  pf_log
#  the graph

ApiConfig.api_key = '2Rm31pJHCmclw6DxyaQU4HUMGoklz04cRC3EZoP8uGnk5eYw6FuHKp3Y4rWCfZ1p' \
                    'zv3K378hCtPMXP1tLDJFyP7bfzF3dB2QEPwilXusYkU8mnM5wlszDTjzSv9bG3ZF'

base = 'BTC'
quote = 'USD'
deviation = 0.0002
interval = 900
beginning_balance = [(quote, 100000)]  # [(quote, 100000), (base, 10)]
trade_volume = beginning_balance[0][1] * 0.2
time_delta = 100
end_date = 1603359857

# same data which will be pulled during backtesting
data_pre = sdk.Data().get_historical_vwap(base=base, quote=quote, interval=interval,
                                          start_date=end_date - time_delta * interval, end_date=end_date)

# analysis of historic data for own use and interest
min_val = data_pre['Price'].min(axis=0)
max_val = data_pre['Price'].max(axis=0)
median_val = data_pre['Price'].median(axis=0)
mean = data_pre['Price'].mean(axis=0)
std_val = data_pre['Price'].std(axis=0)

print(f"min:       {min_val}")
print(f"max:       {max_val}")
print(f"median:    {median_val}")
print(f"mean:      {mean}")
print(f"std. dev.  {std_val}")

# use historic data to determine sensible entry and exit points within the given data set
# percentile of historic data => finds the lowest 20th value 20th from behind
buy_price = data_pre['Price'].quantile(0.2)
# percentile of historic data => finds the highest 20th value; 20th from start
sell_price = data_pre['Price'].quantile(0.8)

simple_strat = SimpleStrategy(base=base, quote=quote, interval=interval, buy_price=buy_price, sell_price=sell_price,
                              trade_volume=trade_volume)

# pf: Portfolio
# pf_log: Portfolio Funds and Value for every historical data input
# data: the historic data used (same as above) just to check and dev purposes only
pf, pf_log, data = BackTesting().backtest(strategy=simple_strat,
                                          beginning_balance=beginning_balance,
                                          end_time=end_date,
                                          time_delta=100,
                                          fees_bp=20,
                                          slippage=2)

equity = pf_log[f'Total Value in {quote}']

# still looks like bad but shows the essentials; just to show the results
equity.plot()
plt.show()
