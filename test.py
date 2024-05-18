import os
from bot_variables import BotVariables as BV 

print('Installing requirements...')
os.system('pip install -r requirements.txt')
print('\n')
good = True

# Perform tests on the `ByBitBackend` class.
BV.BBB.init_session(0, BV.BBB.dev_pub, BV.BBB.dev_secret)

print('`get_users_api_key_information`:', end='\n\t')
API_KEY_INFO = BV.BBB.get_users_api_key_information(0)

if API_KEY_INFO is None:
    print('Failed. Let Moca know.')
else:
    print(f'Success.\n\tReturned: {API_KEY_INFO}')

ACCOUNT_TYPES = ['UC', 'UU', 'UF', 'SS', 'SC', 'SO', 'SF']
print(f'Iterating through all accounts types({",".join(ACCOUNT_TYPES)}):')

for i in ACCOUNT_TYPES:
    UB = BV.BBB.get_user_balance_from_session(0, i, "USDT")

    if UB is None:
        print(f'\t`get_user_balance_from_session` with account type {i}: Failed. Let Moca know')
        good = False
    else:
        print(f'\t`get_user_balance_from_session` with account type {i}: Success\n\tReturned: {UB}\n\tAccount Type: {i}')
        break # Don't keep going

print('\nTesting `get_total_bs_data_from_session`:')
BS = BV.BBB.get_total_bs_data_from_session(0)
print(f'\tReturned: {BS}')
#if BS[0] == '' or BS[1] == '':
#    print('\t`get_total_bs_data_from_session` failed. Let Moca know.')
#else:
#    print(f'\t`get_total_bs_data_from_session` succeeded:\n\tBuy/Sell Data: {BS}')

print(f'\nTesting `get_total_stock_data_from_session` with interval of `D` (day):')
SD = BV.BBB.get_total_stock_data_from_session(0, "D")
print(f'\tReturned: {SD}')
#if SD[0] == '' or SD[1] == '' or SD[2] == '':
#    print('\t`get_total_stock_data_from_session` failed. Let Moca know.')
#else:
#    print(f'\t`get_total_stock_data_from_session` succeeded:\n\tStock Data: {SD}')

print('\nClosing the session (removing from sessions array).')
BV.BBB.close_all_sessions()

if good:
    print(f'\nSuccess! It all works!')
else:
    print('\nIt does not work :(')
