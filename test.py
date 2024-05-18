import subprocess, os
from bot_variables import BotVariables as BV 

# Perform tests on the `ByBitBackend` class.
BV.BBB.init_session(0, BV.BBB.dev_pub, BV.BBB.dev_secret)

ACCOUNT_TYPES = ['UC', 'UU', 'UF', 'SS', 'SC', 'SO', 'SF']
print(f'Iterating through all accounts types({ACCOUNT_TYPES}):')

for i in ACCOUNT_TYPES:
    print(f'Testing Account Type {i} -> {BV.BBB.get_user_balance_from_session(0, i, "USDT")}')

print(f'Testing `get_total_bs_data_from_session`:\n\tBuy/Sell Data: {BV.BBB.get_total_bs_data_from_session(0)}')

print(f'Testing `get_total_stock_data_from_session` with interval of `D` (day):\n\tStock Data: {BV.BBB.get_total_stock_data_from_session(0, "D")}')

print('Closing the session (removing from sessions array).')
BV.BBB.close_all_sessions()

print(f'Success! It all works!\nGenerating zip in {os.path.expanduser("~")}')
